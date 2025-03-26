from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_author = models.BooleanField(default=False)  # Determines if user can write blogs
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
