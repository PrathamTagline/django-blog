from django.contrib.auth.models import AbstractUser
from django.db import models
def user_profile_image_path(instance, filename):
        return f'users/{instance.id}/profile/{filename}'

class User(AbstractUser):
    # Define the choices for the role field
    ROLE_CHOICES = (
        ('author', 'Author'),
        ('guest', 'Guest'),
    )
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to=user_profile_image_path, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest') # Add the role field to the User model with the choices
    created_at = models.DateTimeField(auto_now_add=True)

   
    def __str__(self):
        return self.username
