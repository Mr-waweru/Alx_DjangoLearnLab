from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class CustomUserManager(BaseUserManager):
    """How to create a regular user"""
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email) # Ensures the email is in a standard format
        user = self.model(email=email, **extra_fields)  # Creates a user instance using the custom user model
        user.set_password(password) # Hashes the password for security
        user.save(using=self._db)   # Saves the user to the database
        return user
    
    """Defines how to create a superuser"""
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        for field in ["is_staff", "is_superuser", "is_active"]:
            if not extra_fields.get(field):
                raise ValueError(f"Superuser must have {field} set to True")
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=60, unique=True)
    username = models.CharField(max_length=15, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = CustomUserManager()

    def __str__(self):
        return f"User <{self.email}>"


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="posts")
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author}"
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")  # Links to a specific post
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Links to the comment's author
    content = models.TextField()  # The comment's text
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the creation time
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set the last update time

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"
