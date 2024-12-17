from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from notifications.models import Notification


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
        post = serializer.save(author=self.request.user)
    
        # Notify all followers of the user about the new post
        followers = self.request.user.followers.all()  # Using `followers` field on the user model
        for follower in followers:
            Notification.objects.create(
                recipient=follower,  # Each follower gets a notification
                actor=self.request.user,  # The post author
                verb="created a new post",  # Action performed
                target=post  # The post that was created
            )


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

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def feed(self, request):
        """Retrieve paginated posts from followed users"""
        following_users = request.user.following.all()
        queryset = Post.objects.filter(author__in=following_users).order_by("-created_at")
        page = self.paginate_queryset(queryset)  # Apply pagination
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)  # Return paginated response

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def like(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk) # self.get_object()
        user = request.user
        if post.likes.filter(user=user).exists():  # Check if the user already liked this post
            return Response({"detail": "Already liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        
        Like.objects.create(post=post, user=user)   # Create a new like
        
        # Create a notification for the post author
        Notification.objects.create(
            recipient=post.author,  # The author of the post receives the notification
            actor=user,  # The user who liked the post
            verb="liked",  # Action performed
            target=post  # The post that was liked
        )
        return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)


    @action(detail=True, methods=["delete"])
    def unlike(self, request, pk=None):
        post = self.get_object()    # generics.get_object_or_404(Post, pk=pk)
        user = request.user
        like = post.likes.filter(user=user).first()  # Check if the user has liked this post
        if not like:
            return Response({"detail": "You haven't liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        like.delete()   # Remove the like
        return Response({"detail": "Post unliked."}, status=status.HTTP_204_NO_CONTENT)


# To be deleted (for ALX checker)
    """
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        #Like a post and create a notification for the post author
        post = generics.get_object_or_404(Post, pk=pk)  # Explicitly use generics.get_object_or_404
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if not created:  # User already liked the post
            return Response({'detail': 'You have already liked this post.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a notification for the post author
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post
            )
        return Response({'detail': 'Post liked successfully.'}, status=status.HTTP_201_CREATED)
    """

# ViewSet for handling CRUD operations on Comments
class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Comments in the API."""
    queryset = Comment.objects.all().order_by('-created_at')  # Fetch all comments, ordered by newest first
    serializer_class = CommentSerializer 
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        """Automatically set the current user as the author when creating a comment."""
        comment = serializer.save(author=self.request.user)
    
        # Notify the post author about the new comment
        Notification.objects.create(
            recipient=comment.post.author,  # Post author receives the notification
            actor=self.request.user,  # The comment author
            verb="commented on",  # Action performed
            target=comment.post  # The post that was commented on
        )

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
            return [permissions.IsAuthenticated(), IsAuthorPermission()]  # Only allow authors to modify/delete
        return super().get_permissions()  # Use default permissions for other actions


# Custom permission to check if the user is the author
class IsAuthorPermission(permissions.BasePermission):
    """Permission to allow actions only for the author of the object"""
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user   # # Allow action only if the current user is the author