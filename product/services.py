from decimal import Decimal

import requests
from bs4 import BeautifulSoup

from common.currency import symbol_to_currency

# url = 'https://kateo.bg/products/glowwa-hair-food-vitamini-za-kosa-za-1-mesec?variant=55414409298306'

class KateoStoreScraper:
    @staticmethod
    def get_price(url) -> dict or None:

        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        result = {}

        price_tag = soup.find('span', class_='price')
        title_tag = soup.find('h1')
        description_formatter = soup.find('rte-formatter')


        if price_tag:
            raw_text = price_tag.get_text(strip=True)
            if not raw_text:
                return result
            currency_symbol = raw_text[0]
            currency = symbol_to_currency(currency_symbol)
            price_text = raw_text[1:]
            price_text = price_text.replace(',', '.')
            price_text = price_text.strip()
            price = Decimal(price_text)

            if currency:
                result['currency'] = str(currency)
            if price:
                result['price'] = price

        if title_tag:
            result['title'] = title_tag.get_text(strip=True)[:100]

        if description_formatter:
            p_description = description_formatter.find_next('p')
            if p_description:
                result['description'] = p_description.get_text(strip=True)

        return result
