from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a regular user. Username defaults to the email.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        username = extra_fields.get('username', email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
        
        
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser. Username defaults to the email.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True) 
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # e.g., ['first_name', 'last_name']

    def __str__(self):
        return self.email