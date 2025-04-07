from django.shortcuts import render, redirect

from blogs.models import Blog
from users.models import User

from .forms import LoginForm, RegisterForm

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('login')  # Redirect to login page
    else:
        form = RegisterForm()
    
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.user  # Access the authenticated user from the form
            login(request, user)

            request.session['user_id'] = user.id
            request.session['user_username'] = user.username
            request.session['user_email'] = user.email
            request.session['user_role'] = user.role
            request.session['user_image'] = user.image.url if user.profile_image else None

            return redirect('blogs')

    return render(request, 'users/login.html', {'form': form})

# Logout the user
def user_logout(request):
    logout(request) # Logout the user
    request.session.flush()  # Clear the session

    return redirect('login') # Redirect to the login page

# User profile
@login_required # Ensure that the user is logged in
def profile(request):

    user = User.objects.get(id=request.session.get("user_id")) # Get the user by the session user_id
    user_blogs = Blog.objects.filter(author=user)  # Get the blogs by the user

    context = {
        "user": user,
        "user_blogs": user_blogs,
    }
    return render(request, "users/profile.html", context)
