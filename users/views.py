from .models import User
from .serializers import UserRegisterSerializer, UserLoginSerializer, ForgotPasswordSerializer, ResetPasswordSerializer
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import  redis_client, generate_reset_token, verify_reset_token


User = get_user_model()

class UserRegistrationView(APIView):
    def post(self, request):
        try:
            serializer = UserRegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "success": True,
                        "message": "User registered successfully",
                        "data": serializer.data,
                        "errors": None,
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {
                    "success": False,
                    "message": "Registration failed",
                    "data": None,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    def post(self, request):
        try:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                return Response(
                    {
                        "success": True,
                        "message": "Login successful",
                        "data": serializer.validated_data,
                        "errors": None,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {
                    "success": False,
                    "message": "Login failed",
                    "data": None,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ForgotPasswordView(APIView):
    def post(self, request):
        try:
            serializer = ForgotPasswordSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data["email"].lower().strip()
                user = User.objects.filter(email=email).first()
                if not user:
                    return Response(
                        {"success": False, "message": "User not found", "data": None, "errors": None},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                # Generate and store token in Redis
                token = generate_reset_token(email)

                # Normally you’d email this, but for now we return it in response
                return Response(
                    {
                        "success": True,
                        "message": "Password reset token generated (valid 10 minutes)",
                        "data": {"reset_token": token},
                        "errors": None,
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"success": False, "message": "Invalid request", "data": None, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ResetPasswordView(APIView):
    def post(self, request):
        try:
            serializer = ResetPasswordSerializer(data=request.data)
            if serializer.is_valid():
                token = serializer.validated_data["token"]
                new_password = serializer.validated_data["new_password"]

                # Lookup email from Redis by token
                stored_email = verify_reset_token(token)
                if not stored_email:
                    return Response(
                        {"success": False, "message": "Invalid or expired token", "data": None, "errors": None},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                user = User.objects.filter(email=stored_email).first()
                if not user:
                    return Response(
                        {"success": False, "message": "User not found", "data": None, "errors": None},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                # Reset password
                user.set_password(new_password)
                user.save()

                # # Delete token so it can’t be reused
                # get_redis_client.delete(f"reset_token:{token}")
                redis_client.delete(token)

                return Response(
                    {"success": True, "message": "Password reset successful", "data": None, "errors": None},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"success": False, "message": "Invalid request", "data": None, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
