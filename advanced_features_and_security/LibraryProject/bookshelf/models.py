from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, date_of_birth, password, **extra_fields):
        if not email:
            raise ValueError("Email field must be set")
        if not date_of_birth:
            raise ValueError("Date of birth field must be set")
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, date_of_birth=date_of_birth)
        user.set_password(password)
        return user
    
    def create_superuser(self, username, email, date_of_birth, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not date_of_birth:
            raise ValueError("Date of birth is required")
        
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be staff')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be Superuse')
        
        return self.create_superuser(username, email, date_of_birth, password, **extra_fields)


class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField()

    objects = CustomUserManager()


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publication_year = models.IntegerField(null=True)

    class Meta:
        permissions = [
            ("can_view", "Can view book"),  # (first item)-> codename used in code (e.g., in views or templates) to check if a user has that permission.
            ("can_create", "Can create book"),  # (second item)-> human-readable name, which appears in the Django admin.
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]

    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}, Publication_Year: {self.publication_year}"
    
