from django.shortcuts import render, redirect

from blogs.models import Blog
from users.models import User

from .forms import LoginForm, RegisterForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Register new users
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid(): # Check if the form is valid
            form.save()
            return redirect('login') #redirect to login page
        
    else: # If the form is not valid, render the register page
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})

# Login existing users
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid(): # Check if the form is valid
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            
            try: # Authenticate the user
                user = User.objects.get(email=email) # Get the user by email
                user = authenticate(request, username=user.username, password=password) # Authenticate the user

                # If the user is not None, login the user
                if user is not None:
                    login(request, user)

                    # Set the session variables for the user details
                    request.session['user_id'] = user.id
                    request.session['user_username'] = user.username
                    request.session['user_email'] = user.email
                    request.session['user_role'] = user.role

                    return redirect('blogs') # Redirect to the blogs page
            
            except User.DoesNotExist: # If the user does not exist, pass
                pass

    else: # If the form is not valid, render the login page
        form = LoginForm()
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
