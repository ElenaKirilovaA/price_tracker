from django.db import models

class CurrencyChoices(models.TextChoices):
    EUR = 'EUR', 'EUR'
    USD = 'USD', 'USD'
    GBP = 'GBP', 'GBP'
