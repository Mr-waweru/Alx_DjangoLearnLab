from .serializers import CustomUserSerializer, RegisterSerializer, LoginSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from django.contrib.auth import get_user_model
from rest_framework.views import APIView

User = get_user_model()

# View for user registration
"""Handles user registration"""
class RegisterView(CreateAPIView):
    """API endpoint to register new users."""
    queryset = User.objects.all()   # Retrieve all users
    serializer_class = RegisterSerializer   # Use the RegisterSerializer to validate input
    permission_classes = [permissions.AllowAny] # Allow anyone to access this endpoint


# View for user login
class LoginView(ObtainAuthToken):
    """API endpoint for user login and token generation"""
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """Handle login requests by validating credentials and returning a token"""

        # Validate the input using the serializer
        data = request.data
        serializer = self.serializer_class(data=data, context={
            "request": request
        })
        serializer.is_valid(raise_exception=True)

        # Get the validated user
        user = serializer.validated_data["user"]

        # Retrieve or create an authentication token for the user
        token, created = Token.objects.get_or_create(user=user)

        # Return the token and user details as a response
        return Response(
            {
                "token": token.key, # Authentication token
                "user_id": user.pk, # User ID
                "username": user.username   # Username
            },
            status=status.HTTP_200_OK
        )
    

# View for retrieving user details
class UserDetailView(RetrieveAPIView):
    """API endpoint to retrieve details of a specific user"""
    queryset = User.objects.all()   # Query all users
    serializer_class = CustomUserSerializer # Use CustomUserSerializer to structure the output
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class FollowUserView(generics.GenericAPIView):
    """API endpoint to follow another user"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args,**kwargs):
        """Handle requests to follow a user"""
        user_to_follow_id = request.data.get("user_id") # Get the ID of the user to follow
        
        try:
            # Find the user by ID
            user_to_follow = User.objects.get(id=user_to_follow_id)
        except User.DoesNotExist:
            return Response({"error: User does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Prevent users from following themselves
        if user_to_follow == request.user:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Add the user to the current user's following list
        request.user.following.add(user_to_follow)
        return Response({"status": "Following"}, status=status.HTTP_201_CREATED)
    

# View for unfollowing a user
class UnfollowUserView(APIView):
    """API endpoint to unfollow a user"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args,**kwargs):
        """Handle requests to unfollow a user"""
        user_to_unfollow_id = request.data.get("user_id") # Get the ID of the user to unfollow

        try:
            # Find the user by ID
            user_to_unfollow = User.objects.get(id=user_to_unfollow_id)
        except User.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Prevent users from unfollowing themselves
        if user_to_unfollow == request.user:
            return Response({"error": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Remove the user from the current user's following list
        request.user.following.remove(user_to_unfollow)
        return Response({"status": "Unfollowed"}, status=status.HTTP_204_NO_CONTENT)