from django.shortcuts import get_object_or_404, render
from .models import Blog, Category

def blogs(request):
    all_blogs = Blog.objects.select_related('category').all()
    all_categories = Category.objects.values('name')

    context = {
        'all_blogs': all_blogs,
        'all_categories': all_categories
    }
    return render(request, 'blogs/blog_posts.html', context)

def blog_detail(request, slug):
    blog = get_object_or_404(Blog,slug=slug)
    return render(request, 'blogs/blog_post_detials.html', {'blog': blog})



