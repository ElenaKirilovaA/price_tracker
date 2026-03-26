import random
from decimal import Decimal

import requests
from bs4 import BeautifulSoup
from django.conf import settings

from common.currency import symbol_to_currency

# url = 'https://kateo.bg/products/sacha-care-casse-control-komplekt-za-kosa-protiv-nakasvane-500ml?variant=55511543218562'

def get_price(url: str) -> dict or None:
    if settings.SCRAPER_TEST_MODE:
        price_random = random.randint(20, 150)
        price = Decimal(str(price_random))
        return {'price': price, 'currency': 'EUR'}

    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    price_tag = soup.select_one('span.price:-soup-contains("€")')
    result = {}

    if price_tag:
        raw_text = price_tag.get_text(strip=True)

        if not raw_text:
            return result

        currency_symbol = raw_text[0]
        currency = symbol_to_currency(currency_symbol)
        price_text = raw_text.replace('€', '').replace(',', '.')
        price_text = price_text.strip()
        price = Decimal(price_text)

        if currency:
            result['currency'] = str(currency)
        if price:
            result['price'] = price

    return result


class KateoStoreScraper:
    @staticmethod
    def get_product_info(url: str) -> dict or None:

        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        result = {}

        price_tag = get_price(url)
        title_tag = soup.find('h1')
        description_formatter = soup.find('rte-formatter')


        if price_tag:
            result = price_tag

        if title_tag:
            result['title'] = title_tag.get_text(strip=True)[:100]

        if description_formatter:
            p_description = description_formatter.find_next('p')
            if p_description:
                result['description'] = p_description.get_text(strip=True)

        return result
