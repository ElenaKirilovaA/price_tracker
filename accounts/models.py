

from django.db import models
from django.contrib.auth import models as auth_models

from accounts.managers import AppUserManager



# Create your models here.


class AppUser(auth_models.AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
    )
    favourite_product = models.ManyToManyField(
        'product.Product',
        blank=True,
        related_name='users_favorite',
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Use the custom manager that knows how to create users with email as username
    objects = AppUserManager()



class Profile(models.Model):
    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )
    avatar = models.URLField(
        null=True,
        blank=True,
    )
    user = models.OneToOneField(
        to=AppUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    objects = models.Manager()

    def __str__(self):
        return f"{self.user.get_full_name()}\'s profile"


