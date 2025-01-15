from django.contrib import admin
from django.urls import path
from .views import RegisterView, LoginView, ResetpasswordView, LogoutView, BookView, DeleteView, UpdateView, BorrowView


urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name="register"),
    path('auth/login/', LoginView.as_view(), name="login"),
    path('auth/password/reset/', ResetpasswordView.as_view(), name="resetpassword"),
    path('auth/logout/', LogoutView.as_view(), name="logout"),
    path('auth/books/', BookView.as_view(), name='add-book'),
    # path('auth/books/<int:id>', DeleteView.as_view(), name='delete-book'),
    path('auth/books/<int:id>', UpdateView.as_view(), name='update-book'),
    path('auth/borrow/', BorrowView.as_view(), name='borrow-book'),
]

 