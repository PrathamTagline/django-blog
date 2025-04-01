from django import forms
from django.contrib.auth.forms import UserCreationForm # Import the UserCreationForm for the register form
from .models import User

# Create the login form
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

# Create the register form
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']
