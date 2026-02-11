from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models


from alert.managers import AlertManager, ArchiveAlertManager
from catalog.models import Category
from common.choices import CurrencyChoices
from common.currency import convert_to_eur
from common.mixins import CreatedAtMixin
from product.models import Product


# Create your models here.

class Alert(CreatedAtMixin):
    started_price = models.DecimalField(
        null=True,
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0.02), # TODO exclude triggered_price == 0.00
        ]
    )
    target_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01),

        ]
    )
    triggered_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01),
        ],
        blank=True,
        null=True,
    )
    email = models.EmailField()
    message = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        default=True,
    )
    counter_checks = models.PositiveSmallIntegerField(
        default=0,
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='alerts',
    )
    objects = AlertManager()


    @property
    def price_is_dropped(self) -> bool:
        return self.product.current_price <= self.target_price


    def clean(self) -> None:
        super().clean()

        if self.target_price is not None and self.started_price is not None:
            if self.target_price >= self.product.current_price:
                raise ValidationError({
                    'target_price': 'Target price must be less than started_price.'
                })


    def save(self, *args, **kwargs) -> None:

        if not self.started_price:
            self.started_price = self.product.current_price

        if self.price_is_dropped and not self.triggered_price:
            self.triggered_price = self.product.current_price

        super().save(*args, **kwargs)


    def __str__(self):
        return self.message or (f'Price of {self.product.title} has dropped!\n'
                                f'Status: {self.product}')


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'target_price'],
                name='product_target_price_constraint'
            )
        ]


class ArchiveAlert(models.Model):
    product_title = models.CharField(
        max_length=100,
    )
    started_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0.02)
        ]
    )
    target = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    triggered_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01),
        ],
        blank=True,
        null=True,
    )
    product_currency = models.TextField(
        max_length=3,
        choices=CurrencyChoices,
        default=CurrencyChoices.EUR,
    )
    started_price_eur = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
        null=True,
    )
    triggered_price_eur = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
        null=True,
    )
    counter_checks = models.PositiveSmallIntegerField(
        default=0,
    )
    category_title = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2)
        ],
        null=True,
    )
    alert_created_at = models.DateTimeField()
    alert_finished_at = models.DateTimeField(
        auto_now_add=True,
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='archives',
    )

    objects = ArchiveAlertManager()


    @property
    def saved_money(self) -> str:
        return self.started_price - self.triggered_price


    @property
    def saved_money_eur(self) -> float:
        return self.started_price_eur - self.triggered_price_eur


    @property
    def active_duration(self) -> int:
        return (self.alert_finished_at.date() - self.alert_created_at.date()).days + 1


    def save(self, *args, **kwargs):

        if not self.started_price_eur:
            self.started_price_eur = convert_to_eur(self.started_price, self.product_currency)

        if not self.triggered_price_eur:
            self.triggered_price_eur = convert_to_eur(self.triggered_price, self.product_currency)

        super().save(*args, **kwargs)


    class Meta:
        ordering = ['-alert_finished_at']

