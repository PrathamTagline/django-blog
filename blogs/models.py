from django.db import models
from users.models import User

import random
import string
from django.utils.text import slugify
from django.db import models

def random_string(length=5):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def user_blog_image_path(instance, filename):
    """
    Define the path for blog images.
    Each author's blogs will be stored in their own folder.
    """
    return f'users/{instance.author.id}/blogs/{filename}'
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="blogs")
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags (e.g. #Django, #AI)")
    image = models.ImageField(upload_to=user_blog_image_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug

            # Try to generate a unique slug with random string
            while Blog.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{random_string()}"

            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.blog.title[:30]}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.user.username} liked {self.blog.title[:30]}"
