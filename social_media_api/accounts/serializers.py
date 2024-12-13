from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data["username"],
            email = validated_data["email"],
            password = validated_data["password"]
        )
        return user
    
"""Serializer to handle user login by username or email with a password."""
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False) # Optional field for username
    email = serializers.CharField(required=False)   # Optional field for email
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Validate the login credentials and authenticate the user"""
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        # Ensure at least one identifier (username or email) and password are provided
        if not (username or email) or not password:
            raise serializers.ValidationError('Must include either "username" or "email" and a "password".')
        
        # Authenticate using username or email
        user = None
        if username:
            user = authenticate(username=username, password=password)
        elif email:
            user = authenticate(email=email, password=password)

        # Check if user is authenticated and active
        if not user:
            raise serializers.ValidationError("Invalid credentials provided.")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")
        
        # Attach authenticated user to the validated data
        data["user"] = user
        return data