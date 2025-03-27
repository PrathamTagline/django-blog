from django.contrib import admin
from .models import Blog,Category,Comment,Like
# # Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'category', 'created_at', 'views')
    search_fields = ('title', 'author__username', 'category__name')
    list_filter = ('created_at', 'category')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'blog', 'created_at')
    # search_fields = ('user__username', 'blog__title', 'content')
    # list_filter = ('created_at',)

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'blog', 'created_at')
    search_fields = ('user__username', 'blog__title')

