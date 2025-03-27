from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from .form import SignInForm, SignUpForm, OTPForm
import random

def send_otp(email, otp):
    """Simulate sending OTP to the user's email."""
    # Replace this with actual email sending logic
    print(f"OTP sent to {email}: {otp}")

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully. Please sign in.')
            return redirect('signin')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

def signin_view(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user:
                otp = random.randint(100000, 999999)
                request.session['otp'] = otp
                request.session['user_id'] = user.id
                send_otp(email, otp)
                return redirect('verify_otp')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = SignInForm()
    return render(request, 'users/signin.html', {'form': form})

def verify_otp_view(request):
    if 'otp' not in request.session or 'user_id' not in request.session:
        return redirect('signin')

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            if int(entered_otp) == request.session['otp']:
                user_id = request.session['user_id']
                user = authenticate(request, id=user_id)  # Fetch user by ID
                if user:
                    login(request, user)
                    messages.success(request, 'Successfully signed in!')
                    del request.session['otp']
                    del request.session['user_id']
                    return redirect('home')
            else:
                messages.error(request, 'Invalid OTP.')
    else:
        form = OTPForm()
    return render(request, 'users/verify_otp.html', {'form': form})

def signout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Successfully signed out!')
    return redirect('home')