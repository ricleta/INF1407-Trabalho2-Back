from django.urls import path
from . import views

app_name = 'Seguranca'

urlpatterns = [
    path('login/', views.CustomAuthToken.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.UserRegistrationView.as_view(), name='user-registration'),
    path('forgot_password/', views.ForgotPasswordView.as_view(), name='forgot-password'),
]