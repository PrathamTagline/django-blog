from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .form import OTPForm, SignUpForm, SignInForm
from django.contrib import messages
from django.contrib.auth import get_user_model

import random

def sign_in_view(request):
    if request.method == 'POST':
        form = SignInForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Sign in successful!")
                return redirect('home')  # Replace 'home' with your desired redirect URL
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = SignInForm()
    return render(request, 'users/signin.html', {'form': form})

# filepath: /Users/mac/Desktop/blog/users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import get_user_model

import random

from users.form import OTPForm, SignUpForm

User = get_user_model()  # Ensure this line remains to use the custom user model

def send_otp(email, otp):
    """Simulate sending OTP to the user's email."""
    # Replace this with actual email sending logic
    print(f"OTP sent to {email}: {otp}")

def sign_up_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Save user data in session temporarily
            request.session['signup_data'] = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password1'],
            }
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            send_otp(form.cleaned_data['email'], otp)
            return redirect('verify_otp')  # Redirect to OTP verification page
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

def otp_verification_view(request):
    signup_data = request.session.get('signup_data')
    if not signup_data:
        return redirect('signup')  # Redirect to signup if no data in session

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            if int(entered_otp) == request.session.get('otp'):
                # Create and save the user
                user = User.objects.create_user(
                    username=signup_data['username'],
                    email=signup_data['email'],
                    password=signup_data['password']
                )
                login(request, user)
                messages.success(request, "Sign up successful and OTP verified!")
                # Clear session data
                del request.session['signup_data']
                del request.session['otp']
                return redirect('home')  # Replace 'home' with your desired redirect URL
            else:
                messages.error(request, "Invalid OTP.")
    else:
        form = OTPForm()
    return render(request, 'users/verify_otp.html', {'form': form})