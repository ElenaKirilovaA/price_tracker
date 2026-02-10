from decimal import Decimal
from django import template
from common.choices import CurrencyChoices

register = template.Library()

@register.simple_tag
def price_with_currency(value: Decimal, currency) -> str:
    mapper = {
        CurrencyChoices.EUR: f'{value}€',
        CurrencyChoices.USD: f'${value}',
        CurrencyChoices.GBP: f'£{value}'
    }

    if value is None:
        return '-'

    return mapper.get(currency) if currency else f'{value}{currency}'
