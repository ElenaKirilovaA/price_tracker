from decimal import Decimal

from common.choices import CurrencyChoices

currency_mapper = {
    CurrencyChoices.EUR: Decimal('1.00'), # Decimal('str') -> точно изчисляване, без грешки от float
    CurrencyChoices.USD: Decimal('0.92'),
    CurrencyChoices.GBP: Decimal('1.17')
}

def convert_to_eur(price: Decimal, currency) -> Decimal:
    rate = currency_mapper.get(currency) * price
    return rate.quantize(Decimal('0.01'))  # != .:2f-> пази стойността такава и в базата
