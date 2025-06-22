from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model



class CustomUser(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email
    def get_short_name(self):
        return self.email
    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return True
    def has_module_perms(self, app_label):
        return True
    
class Profile(models.Model):
    user= models.OneToOneField(CustomUser,related_name="profile", on_delete=models.CASCADE) 
    mobile_number = models.CharField(max_length=15)
    avatar = models.ImageField(upload_to="profile_avatar", null=True)

    def __str__(self):
        return self.user.email