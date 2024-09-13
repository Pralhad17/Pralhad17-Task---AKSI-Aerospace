from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Superadmin', 'Superadmin'),
        ('Admin', 'Admin'),
        ('Superuser', 'Superuser'),
        ('User', 'User'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='User')
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_users')
