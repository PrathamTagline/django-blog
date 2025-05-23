from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('allposts', views.all_blogs, name='blogs'),
    path('post/<slug:slug>', views.blog_post_details, name='blog_detail'),
    path('create/', views.add_blog, name='create_blog'),
    path('edit/<int:blog_id>/', views.edit_blog, name='edit_blog'),
    path('delete/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path('post/<int:blog_id>/add_comment/', views.add_comment, name='add_comment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)