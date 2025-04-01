from django.urls import path
from . import views

urlpatterns = [
    path('allposts', views.blogs, name='blogs'),
    path('post/<slug:slug>', views.blog_detail, name='blog_detail'),
     path('create/', views.add_blog, name='create_blog'),
    path('edit/<int:blog_id>/', views.edit_blog, name='edit_blog'),
    path('delete/<int:blog_id>/', views.delete_blog, name='delete_blog'),
]
