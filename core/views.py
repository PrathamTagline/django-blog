from django.shortcuts import render
from django.http import HttpResponse
from blogs.models import Blog
# Create your views here.
def home(request):
    recent_blogs = Blog.objects.all().order_by('-created_at')[:5] # Get the 4 most recent blogs
    context = {
        'recent_blogs': recent_blogs
    }
    return render(request, 'core/home.html', context)