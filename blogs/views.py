from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from blogs.forms import BlogForm
from .models import Blog, Category,Comment,Like
from users.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# display all blogs and categories
def all_blogs(request):
    
    all_blogs = Blog.objects.select_related('category', 'author').all() # Get all blogs with the category and author
    all_categories = Category.objects.values('name') # Get all categories
    
    context = {
        'all_blogs': all_blogs,
        'all_categories': all_categories
    }
    return render(request, 'blogs/all_blog_posts.html', context)

# post details and comments of the blog post 
def blog_post_details(request, slug):
    blog = get_object_or_404(Blog,slug=slug) # Get the blog by slug
    comments = Comment.objects.filter(blog=blog) # Get all comments for the blog post (if any exist in the database for the perticular blog post)
    return render(request, 'blogs/blog_post_detials.html', {'blog': blog, 'comments': comments})


# add new blog post (only for author role users can access this page ) 
@login_required
def add_blog(request):
    if request.user.role == 'author': # Check if the user is an author
        if request.method == 'POST': # If the form is submitted
            form = BlogForm(request.POST, request.FILES) # Get the form data
            if form.is_valid():
                blog = form.save(commit=False)
                blog.author = request.user  # Set the author to the logged-in user
                blog.save()
                return redirect('blogs')  # Redirect to the blog list page
        else:
            form = BlogForm() # Create a new form
        return render(request, 'blogs/add_blog.html', {'form': form})
    else:
        return HttpResponse("You are not authorized to access this page.") # If the user is not an author, return an error message


# edit blog post (only for author role users can access this page )
@login_required
def edit_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id) # Get the blog by ID

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
        form = BlogForm(instance=blog) # Create a new form with the blog data

    return render(request, 'blogs/edit_blog.html', {'form': form, 'blog': blog})

# delete blog post (only for author role users can access this page and only author can delete their own blog post)
@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id) # Get the blog by ID

    # Check if the logged-in user is the author of the blog
    if blog.author != request.user:
        return HttpResponseForbidden()

    blog.delete() # Delete the blog
    messages.success(request, "Blog deleted successfully!")
    return redirect('profile')



@login_required
def add_comment(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)  # Get the blog by ID (if it exists)
    if request.method == 'POST':
        content = request.POST.get('content').strip()  # Get the comment content from the form
        if content:
            if content == "":
                messages.error(request, "Comment cannot be empty.")
                return redirect('blog_detail', slug=blog.slug)
    
            # Create a new comment and associate it with the blog and user
            Comment.objects.create(
                blog=blog,
                user=request.user,
                content=content
            )
    return redirect('blog_detail', slug=blog.slug)  # Redirect to the blog detail page with the slug