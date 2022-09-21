from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.dispatch import receiver
from django.urls import reverse
from django.core.mail import send_mail  

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, password, first_name, last_name,**other_fields):
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, password, first_name, last_name, **other_fields)

    def create_user(self, email, password, first_name, last_name, **other_fields):

        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', True)    
        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')  
          
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name,**other_fields)
        user.set_password(password)
        user.save()
        return user

class ExtUser(AbstractBaseUser, PermissionsMixin):
    mobile_no = models.CharField(max_length=11, null=True, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    joining_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_mobile_no_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)   
    address = models.TextField(null=True, blank=True)
    # permissions = jsonfield.JSONField(null=True, blank=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name_plural = "Users"

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
