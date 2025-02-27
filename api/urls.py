from django.contrib import admin
from django.urls import path
from .views import RegisterView, LoginView, ResetpasswordView, LogoutView, BookView, DeleteView, UpdateView, BorrowView, ReserveView, RenewBorrowView, ReturnBookView, CancelReservationView, HistoryView, FineView, PaymentProcessView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name="register"),
    path('auth/login/', LoginView.as_view(), name="login"),
    path('auth/password/reset/', ResetpasswordView.as_view(), name="resetpassword"),
    path('auth/logout/', LogoutView.as_view(), name="logout"),
    path('auth/books/', BookView.as_view(), name='add-book'),
    # path('auth/books/<int:id>', DeleteView.as_view(), name='delete-book'),
    path('auth/books/<int:id>', UpdateView.as_view(), name='update-book'),
    path('borrow/', BorrowView.as_view(), name='borrow-book'),
    path('return/', ReturnBookView.as_view(), name="return-book"),
    path('reserve/', ReserveView.as_view(), name="reserve-book"),
    path('renew/', RenewBorrowView.as_view(), name="renew-book"),
    path('history/', HistoryView.as_view(), name="borrow-history"),
    path('cancel/<int:id>', CancelReservationView.as_view(), name="cancel-reserve"),
    path('fines/', FineView.as_view(), name="fine"),
    path('payments/', PaymentProcessView.as_view(), name='payment')
]

 