from django.contrib import admin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_staff", "is_superuser", "is_active") # Columns to display
    list_filter = ("is_superuser", "is_staff", "is_active") # Adds filters for these fields

admin.site.register(CustomUser, CustomUserAdmin)