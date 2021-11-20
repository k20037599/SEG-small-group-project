from django.contrib import admin

"""Configuration for the admin interface for clubs"""

from django.contrib import admin
from .models import User

"""Configuration for the admin interface for users"""
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # This lets us specify the attributes that are included in the user table.
    list_display = ["first_name", "last_name", "email", "is_active", "bio", "experience_level", "user_type", "personal_statement"]
