from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager

class User(AbstractUser):
    GENDER_TYPES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    username = models.CharField(max_length=10,unique=False, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=50, unique=True, null=False)
    show_name = models.CharField(max_length=30, null=True, blank=True)
    gender = models.CharField(max_length=2, choices=GENDER_TYPES, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    is_company = models.BooleanField(default=False)
    company_name = models.CharField(max_length=50, null=True, blank=True)
    company_address = models.CharField(max_length=50, null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ()

    def __str__(self):
        return self.email