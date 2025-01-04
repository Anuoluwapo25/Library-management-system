from django.contrib import admin
from django.urls import path
from .views import RegisterAPIView


urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name='register')
    #   path = ('auth/login/', login.views.as_view(), name=login)
]

