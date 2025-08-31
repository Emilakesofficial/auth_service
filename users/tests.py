from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthTests(APITestCase):
    def setUp(self):
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.forgot_password_url = reverse("forgot-password")
        self.reset_password_url = reverse("reset-password")

        self.user_data = {
            "full_name": "John Doe",
            "email": "john@example.com",
            "password": "StrongPass1@",
            "confirm_password": "StrongPass1@",
        }

        self.user = User.objects.create_user(
            email="existing@example.com",
            full_name="Existing User",
            password="TestPass123@",
        )

    def test_register_success(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])

    def test_register_password_mismatch(self):
        data = self.user_data.copy()
        data["confirm_password"] = "WrongPass1@"
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])

    def test_login_success(self):
        response = self.client.post(
            self.login_url, {"email": "existing@example.com", "password": "TestPass123@"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertIn("access_token", response.data["data"])

    def test_login_invalid_credentials(self):
        response = self.client.post(
            self.login_url, {"email": "existing@example.com", "password": "WrongPass1@"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])

    @patch("users.views.generate_reset_token")
    def test_forgot_password_success(self, mock_generate_token):
        mock_generate_token.return_value = "mock-token-123"
        response = self.client.post(self.forgot_password_url, {"email": "existing@example.com"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["reset_token"], "mock-token-123")

    def test_forgot_password_user_not_found(self):
        response = self.client.post(self.forgot_password_url, {"email": "unknown@example.com"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data["success"])

    @patch("users.views.verify_reset_token")
    @patch("users.views.redis_client")
    def test_reset_password_success(self, mock_redis, mock_verify_token):
        mock_verify_token.return_value = "existing@example.com"
        payload = {
            "token": "mock-token-123",
            "new_password": "NewPass123@",
            "confirm_password": "NewPass123@",
        }
        response = self.client.post(self.reset_password_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        mock_redis.delete.assert_called_once_with("reset_token:mock-token-123")

        # Verify password actually changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewPass123@"))

    @patch("users.views.verify_reset_token")
    def test_reset_password_invalid_token(self, mock_verify_token):
        mock_verify_token.return_value = None
        payload = {
            "token": "invalid-token",
            "new_password": "NewPass123@",
            "confirm_password": "NewPass123@",
        }
        response = self.client.post(self.reset_password_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])
