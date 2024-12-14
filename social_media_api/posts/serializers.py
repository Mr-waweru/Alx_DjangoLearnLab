from .models import Post, Comment, Like
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)  # Display author's username
    comments = serializers.StringRelatedField(many=True, read_only=True)  # Display comment info
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)  # Count of likes for the post

    class Meta:
        model = Post
        fields = ["id", "author", "title", "content", "created_at", "updated_at", "comments", "likes_count"]
        read_only_fields = ["author", "created_at", "updated_at"]   # Specifies fields that cannot be updated by the client

    def create(self, validated_data):
        """Overriding the create method to associate the authenticated user with the post"""
        validated_data["author"] = self.context["request"].user # Set the author as the logged-in user
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)  # Display author's username
    post_title = serializers.CharField(source="post.title", read_only=True)  # Include post title in the response

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["author", "created_at", "updated_at"]

    def create(self, validated_data):
        """Overriding the create method to associate the authenticated user with the comment"""
        validated_data["author"] = self.context["request"].user  # Set the author as the logged-in user
        return super().create(validated_data)


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Display user's username
    post_title = serializers.CharField(source="post.title", read_only=True)  # Include post title in the response

    class Meta:
        model = Like
        fields = ["id", "post", "post_title", "user", "created_at", "updated_at"]
        read_only_fields = ["user", "created_at", "updated_at"] # Fields are set by the system and not modifiable by the client.

    def create(self, validated_data):
        """Overriding the create method to associate the authenticated user with the like"""
        validated_data["user"] = self.context["request"].user  # Set the user as the logged-in user
        return super().create(validated_data)