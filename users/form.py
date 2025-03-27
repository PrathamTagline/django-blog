from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

# filepath: /Users/mac/Desktop/blog/users/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SignInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

# filepath: /Users/mac/Desktop/blog/users/forms.py
from django import forms

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'placeholder': 'Enter OTP'}))
