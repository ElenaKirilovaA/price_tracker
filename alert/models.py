from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models
from alert.querysets import ActiveAlertQuerySet, ArchiveAlertQuerySet
from catalog.models import Category
from common.choices import CurrencyChoices
from common.mixins import CreatedAtMixin
from product.models import Product


# Create your models here.
UserModel = get_user_model()


class Alert(CreatedAtMixin):
    started_price = models.DecimalField(
        null=True,
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.01')), # track with started price 0.00 intentionally exclude
        ]
    )
    target_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.01')),

        ]
    )
    triggered_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.01')),
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
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='alerts',
    )
    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name='alerts'
    )
    objects = ActiveAlertQuerySet.as_manager()


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
                fields=['product', 'target_price', 'user'],
                name='product_target_price_constraint',
                violation_error_message='You already have a track with this product and this target price.'
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
            MinValueValidator(Decimal('0.01')),
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
            MinValueValidator(Decimal('0.01')),
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
    user = models.ForeignKey(
        to=UserModel,
        on_delete=models.CASCADE,
        related_name='archives'
    )

    objects = ArchiveAlertQuerySet.as_manager()


    @property
    def saved_money(self) -> Decimal:
        return self.started_price - self.triggered_price


    @property
    def saved_money_eur(self) -> Decimal:
        return self.started_price_eur - self.triggered_price_eur


    @property
    def active_duration(self) -> int:
        return (self.alert_finished_at.date() - self.alert_created_at.date()).days


    class Meta:
        ordering = ['-alert_finished_at']



class PriceTimeline(models.Model):
    """
    Every time the simulation for price drop is checked,
    the class is adding a new row in db. Model is timeline snapshot.
    """

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    checked_at = models.DateTimeField(
        auto_now_add=True,
    )
    alert = models.ForeignKey(
        to=Alert,
        on_delete=models.CASCADE,
        related_name='price_timelines'
    )

    class Meta:
        ordering = ['checked_at']


class PriceTimelineArchived(models.Model):
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    checked_at = models.DateTimeField()
    history_alert = models.ForeignKey(
        to=ArchiveAlert,
        on_delete=models.CASCADE,
        related_name='history_alerts'
    )
