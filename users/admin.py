from django.contrib import admin
from .models import User
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_author', 'created_at')
    search_fields = ('username', 'email')
    list_filter = ('is_author', 'created_at')