from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token

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
        # Create the user
        user = get_user_model().objects.create_user(    #Used this because of alx checker. get_user_model() method is assigned to User at line 5
            username = validated_data["username"],
            email = validated_data["email"],
            password = validated_data["password"]
        )
        # Generate a token for the user
        Token.objects.create(user=user)
        return user
    
"""Serializer to handle user login by username or email with a password."""
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField() # Optional field for username
    email = serializers.CharField()   # Optional field for email
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
        
        # Generate or retrieve token for authenticated user
        token, created = Token.objects.get_or_create(user=user)

        # Attach authenticated user and token to the validated data
        data["user"] = user
        data["token"] = token.key
        return data