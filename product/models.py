from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify
from catalog.models import Category, Tag
from common.choices import CurrencyChoices
from common.mixins import BaseInfoTitle, CreatedAtMixin, BaseInfoDescription
from decimal import Decimal


# Create your models here.
UserModel = get_user_model()

class Product(BaseInfoTitle, BaseInfoDescription, CreatedAtMixin):
    slug = models.SlugField(
        unique=True,
        max_length=100,
        blank=True,
    )
    url = models.URLField(

    )
    current_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.00'))
        ],
    )
    currency = models.CharField(
        max_length=3,
        choices=CurrencyChoices,
        default=CurrencyChoices.EUR,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.PROTECT,
        related_name='products',
    )
    tag = models.ManyToManyField(
        to=Tag,
        related_name='products',
        blank=True,
        help_text='choose a tag or create your own',
    )
    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )


    @property
    def is_tracking(self):
        return self.alerts.filter(is_active=True).exists()


    def save(self, *args, **kwargs):
        if not self.slug:
            current_str = f'{self.title}-{self.category.title}'
            self.slug = slugify(current_str[:100])

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.title} - {self.current_price} {self.currency}"
