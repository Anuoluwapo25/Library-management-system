from django.contrib import admin
from django.urls import path
from .views import RegisterView, LoginView, ResetpasswordView, LogoutView, BookView


urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name="register"),
    path('auth/login/', LoginView.as_view(), name="login"),
    path('auth/password/reset/', ResetpasswordView.as_view(), name="resetpassword"),
    path('auth/logout/', LogoutView.as_view(), name="logout"),
    path('auth/books/', BookView.as_view(), name='add-book')
]

