from django.contrib import admin
from django.urls import path
from .views import RegisterView


urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register')
    #   path = ('auth/login/', login.views.as_view(), name=login)
]

