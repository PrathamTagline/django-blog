from django.urls import path
from . import views

urlpatterns = [
    path('allposts', views.blogs, name='blogs'),
    path('post/<slug:slug>', views.blog_detail, name='blog_detail'),
]
