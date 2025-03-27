from django.urls import path
from . import views

urlpatterns = [
    path('sign-up/', views.sign_up_view, name='signup'),
    # path('sign-in/', views.sign_in_view, name='signin'),
    path('otp-verification/', views.otp_verification_view, name='otpverification'),
]