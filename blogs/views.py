from django.shortcuts import render
from .models import Blog,Category
# Create your views here.

def blogs(request):
    all_blogs = Blog.objects.all()
    all_categories = Category.objects.values('name')

    context = {
        'all_blogs': all_blogs,
        'all_categories':all_categories
    }
    return render(request, 'blogs/blog_posts.html', context)