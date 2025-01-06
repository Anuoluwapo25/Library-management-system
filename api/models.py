from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    account_type = models.CharField(max_length=10, choices=[('user', 'User'), ('admin', 'Admin')])
    country = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)
    state = models.CharField(max_length=100)
    address = models.TextField()
    phone_number = models.CharField(max_length=20)

    class Meta:
        db_table = 'users'