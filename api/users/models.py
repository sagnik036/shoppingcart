from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager,AbstractUser
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
import random
from django.utils.translation import gettext_lazy as _

# def upload_path(instance ,filename):
#     return '/'.join(['images',str(instance.mobile),filename]) 

#customusernmanager
class CustomUserManager(BaseUserManager):
    def create_user (self,username,password,first_name,last_name, email = None,**extrafields):
        if not username:
            raise ValueError("username Not Provided")
        if not first_name:
            raise ValueError("first_name Not Given")
        
        user = self.model(
                username = username,
                first_name = first_name,
                last_name = last_name,
                password=password,
                **extrafields
            )
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True

        user.save(using=self._db)
        return user
    def create_superuser(self,username,password,first_name,last_name ,**extrafields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username = username,
            first_name = first_name,
            last_name = last_name,
            password=password,
            **extrafields
        )
        user.set_password(password)
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

CHOICES =(
    ("1", "seller"),
    ("2", "customer"),
)

#custom user model
class CustomUser(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(
        unique=True,
        null=True,
        blank=True
    )
    mobile = models.CharField(
        unique=True,
        max_length=10,
        null=True,
        blank=True
    )
    company_name = models.CharField(
        max_length = 50,
        null =True,
        blank=True
    )
    is_staff = models.BooleanField(
        default=False
    )
    is_active = models.BooleanField(
        default=True
    )
    user_type = models.CharField(
        max_length = 50,
        choices = CHOICES
    )
    is_superuser = models.BooleanField(
        default=False
    )
    
    objects = CustomUserManager()


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS =  ['first_name','last_name','password']
        
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
