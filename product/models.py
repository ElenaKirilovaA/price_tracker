from django.core.validators import MinValueValidator
from django.db import models

from django.template.defaultfilters import slugify

from catalog.models import Category, Tag
from common.choices import CurrencyChoices

from common.mixins import BaseInfoTitle, CreatedAtMixin, BaseInfoDescription


# Create your models here.

class Product(BaseInfoTitle, BaseInfoDescription, CreatedAtMixin):
    slug = models.SlugField(
        unique=True,
        max_length=100,
        blank=True,
    )
    url = models.URLField(  )
    current_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01)
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
    )


    @property
    def is_tracking(self):
        return self.alerts.filter(is_active=True).exists()


    def save(self, *args, **kwargs):
        if not self.slug:
            category = self.category.title if self.category else ''
            self.slug = slugify(f"{self.title}-{category}")

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.title} - {self.current_price} {self.currency}"
