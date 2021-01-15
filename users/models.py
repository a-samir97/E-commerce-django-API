from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager

from products.models import Product

class User(AbstractUser):
    USER_TYPES = (
        ('A', 'Admin'),
        ('U', 'User')
    )
    GENDER_TYPES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    username = models.CharField(max_length=10,unique=False, null=True, blank=True)
    img = models.ImageField(null=True, blank=True, upload_to='media/')
    user_type = models.CharField(choices=USER_TYPES, max_length=1, default='U')
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=50, unique=True, null=False)
    show_name = models.CharField(max_length=30, null=True, blank=True)
    gender = models.CharField(max_length=2, choices=GENDER_TYPES, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    is_company = models.BooleanField(default=False)
    company_name = models.CharField(max_length=50, null=True, blank=True)
    company_address = models.CharField(max_length=50, null=True, blank=True)
    is_blocked = models.BooleanField(default=False)
    is_gold = models.BooleanField(default=False)
    favorite_products = models.ManyToManyField(Product)
    following = models.ManyToManyField('User', related_name='followers')
    pass_code = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    global_visa = models.CharField(max_length=50, null=True, blank=True)
    local_visa = models.CharField(max_length=50, null=True, blank=True)
    bank_name = models.CharField(max_length=50, null=True, blank=True)

    # model managers 
    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ()

    def __str__(self):
        return self.first_name + ' ' + self.last_name