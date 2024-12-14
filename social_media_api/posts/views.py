from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 3  # Default number of results per page
    page_size_query_param = 'page_size'  # Allow clients to control the page size
    max_page_size = 10  # Limit the maximum page size



# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for handling CRUD operations on Posts"""
    queryset = Post.objects.all().order_by("-created_at")   # Fetch all posts, ordered by newest first
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]    # # Authenticated users can create/edit, others can only read
    pagination_class = StandardResultsSetPagination

    # Filtering support for search functionality
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "content"]    # Allow searching by title or content

    def perform_create(self, serializer):
        """Automatically set the current user as the author when creating a post."""
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        """Override create method to include a status code for successful creation."""
        serializer = self.get_serializer(data=request.data) # # Deserialize incoming request data
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()    # Retrieve the specific post instance
        self.perform_destroy(instance)  # # Delete the instance
        return Response({"detail": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        """Only the author can edit or delete a post"""
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAuthorPermission()]    # Custom permission for authors
        return super().get_permissions()    # Use default permissions for other actions

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        # Check if the user already liked this post
        if post.likes.filter(user=user).exists():
            return Response({"detail": "Already liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        # Create a new like
        Like.objects.create(post=post, user=user)
        return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete"])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        # Check if the user has liked this post
        like = post.likes.filter(user=user).first()
        if not like:
            return Response({"detail": "You haven't liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        # Remove the like
        like.delete()
        return Response({"detail": "Post unliked."}, status=status.HTTP_204_NO_CONTENT)


# ViewSet for handling CRUD operations on Comments
class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Comments in the API."""
    queryset = Comment.objects.all().order_by('-created_at')  # Fetch all comments, ordered by newest first
    serializer_class = CommentSerializer 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        """Automatically set the current user as the author when creating a comment"""
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)  # Deserialize incoming request data
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)  # Save the data, setting the current user as author
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Retrieve the specific comment instance
        self.perform_destroy(instance)  # Delete the instance
        return Response({"detail": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAuthorPermission()]  # Custom permission for authors
        return super().get_permissions()  # Use default permissions for other actions


# Custom permission to check if the user is the author
class IsAuthorPermission(permissions.BasePermission):
    """Permission to allow actions only for the author of the object"""
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user   # # Allow action only if the current user is the author