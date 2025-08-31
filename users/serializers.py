from rest_framework import serializers
from .models import User
import re
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ["full_name", "email", "password", "confirm_password"]
        
    def validate(self, data):
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        
        # Check if both match
        if password != confirm_password:
            raise serializers.ValidationError({"message": "Password does not match."})
        
        # Set password rules
        if len(password)< 8:
            raise serializers.ValidationError({"message": "Password must be at least 8 characters long"})
        if not re.search(r"[A-Z]", password):
            raise serializers.ValidationError({"message": "Password must contain at least one uppercase letter"})
        if not re.search(r"[a-z]", password):
            raise serializers.ValidationError({"message": "Password must contain at least one lowercase character"})
        if not re.search(r"[0-9]", password):
            raise serializers.ValidationError({"message":"Password must contain at least one numeric number"})
        if not re.search(r"[@!$*?&#%^]", password):
            raise serializers.ValidationError({"message": "Password must contain at least one special character"})
        
        return data
    
    def create(self, validated_data):
        validated_data.pop("confirm_password")  # remove confirm_password, not needed in DB

        user = User.objects.create_user(
            email=validated_data["email"],
            full_name=validated_data["full_name"],
            password=validated_data["password"],
        )
        return user
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        
        user = authenticate(email=email, password=password)
        
        if not user:
            raise serializers.ValidationError({"message": "Invalid credentials"})
        
        if not user.is_active:
            raise serializers.ValidationError({"message": "User is not an active user"})
        
        refresh = RefreshToken.for_user(user)
        return {
            "access_token" : str(refresh.access_token),
            "refresh": str(refresh.access_token),
            "user": {
                "full_name": user.full_name,
                "email" : user.email,
            },
        }

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        password = data.get("new_password")
        confirm_password = data.get("confirm_password")
        
        if password != confirm_password:
            raise serializers.ValidationError({"message": "Password does not match."})
        
        # Set password rules
        if len(password)< 8:
            raise serializers.ValidationError({"message": "Password must be at least 8 characters long"})
        if not re.search(r"[A-Z]", password):
            raise serializers.ValidationError({"message": "Password must contain at least one uppercase letter"})
        if not re.search(r"[a-z]", password):
            raise serializers.ValidationError({"message": "Password must contain at least one lowercase character"})
        if not re.search(r"[0-9]", password):
            raise serializers.ValidationError({"message":"Password must contain at least one numeric number"})
        if not re.search(r"[@!$*?&#%^]", password):
            raise serializers.ValidationError({"message": "Password must contain at least one special character"})
        
        return data
    
    