from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

# Create the login form
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

# Create the register form
class RegisterForm(UserCreationForm):
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ["profile_image", "username", "email", "role"]

    def save(self, commit=True):
        user = super().save(commit=False)  # Save user but don't commit yet
        if commit:
            user.save()  

            # Save profile image after user has an ID
            if self.cleaned_data.get('profile_image'):
                user.profile_image = self.cleaned_data['profile_image']
                user.save()
        
        return user
