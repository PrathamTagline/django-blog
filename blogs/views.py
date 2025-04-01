from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseForbidden
from blogs.forms import BlogForm
from .models import Blog, Category,Comment
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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
    comments = Comment.objects.filter(blog=blog)
    return render(request, 'blogs/blog_post_detials.html', {'blog': blog, 'comments': comments})


@login_required
def add_blog(request):
    if request.user.role == 'author':
        if request.method == 'POST':
            form = BlogForm(request.POST, request.FILES)
            if form.is_valid():
                blog = form.save(commit=False)
                blog.author = request.user  # Set the author to the logged-in user
                blog.save()
                return redirect('blogs')  # Redirect to the blog list page
        else:
            form = BlogForm()
        return render(request, 'blogs/add_blog.html', {'form': form})
    else:
        return HttpResponse("You are not authorized to access this page.")


@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    # Check if the logged-in user is the author of the blog
    if blog.author != request.user:
        messages.error(request, "You are not authorized to edit this blog.")
        return redirect('blogs')  # Redirect to the blog list page

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog updated successfully!")
            return redirect('profile')  # Redirect to the blog detail page
    else:
        form = BlogForm(instance=blog)

    return render(request, 'blogs/edit_blog.html', {'form': form, 'blog': blog})


@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)

    # Check if the logged-in user is the author of the blog
    if blog.author != request.user:
        return HttpResponseForbidden()

    blog.delete()
    messages.success(request, "Blog deleted successfully!")
    return redirect('profile')