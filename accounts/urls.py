
from django.urls import path
from .views import  UserRegistrationView, ChangePassView
from . import views

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.UserUpdateProfile.as_view(), name='profile'),

    path('profile/pass_change/', ChangePassView.as_view(), name='change_pass'),
]
