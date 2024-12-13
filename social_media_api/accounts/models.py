from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email field must be provided")
        email = self.normalize_email(email)
        new_user = self.model(email=email, **extra_fields)
        new_user.set_password(password)
        new_user.save(using=self._db)
        return new_user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        for field in ["is_staff", "is_superuser", "is_active"]:
            if not extra_fields.get(field):
                raise ValueError(f"Superuser must have {field} set to True.")
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)   # upload_to = "" Specifies the directory where uploaded images will be saved.
    followers = models.ManyToManyField("self", symmetrical=False, related_name="following") # 'self' Refers to the same model (CustomUser) for the relationship.
    # symmetrical=False For example, if User A follows User B, it doesn't automatically mean User B follows User A.

    def __str__(self):
        return self.username