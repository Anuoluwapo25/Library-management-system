from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    account_type = models.CharField(max_length=10, choices=[('user', 'User'), ('admin', 'Admin')], default='user')
    country = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)
    state = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)

    class Meta:
        db_table = 'users'

class Author(models.Model):
    name = models.CharField(max_length=255)


    def __str__(self):
        return self.name


class Book(models.Model):
     title = models.CharField(max_length=255)
     author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
     genre = models.CharField(max_length=100)
     description = models.TextField()
     availability = models.BooleanField(default=True)
     created_at = models.DateTimeField(auto_now_add=True)


     def __str__(self):
         return self.title


class Borrow(models.Model):
    dateBorrow = models.DateTimeField(auto_now_add=True)
    borrowedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='borrowed_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrow_records')
    dateReturn = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"{self.borrowedBy.username} borrowed {self.book.title}"