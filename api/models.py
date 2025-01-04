from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Client(AbstractUser):
    email = models.EmailField(max_length=225, unique=True)
    password = models.CharField(max_length=225)
    name = models.CharField(max_length=225)
    country = models.CharField(max_length=100, blank=True)
    countrycode = models.IntegerField(null=True)
    state = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    phoneNumber = models.CharField(max_length=15, blank=True)
    
   
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='client_users'  
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='client_users' 
    )
    
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def __str__(self):
        return self.name