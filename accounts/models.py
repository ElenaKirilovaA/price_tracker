from django.db import models
from django.contrib.auth import models as auth_models

from accounts.managers import AppUserManager


# Create your models here.


class AppUser(auth_models.AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Profile(models.Model):
    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )
    profile_picture = models.ImageField(
        upload_to='profile_images',
        null=True,
        blank=True,
    )
    user = models.OneToOneField(
        to=AppUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    objects = AppUserManager()

    def __str__(self):
        return f'{self.user.full_name()}\'s profile'