import random
from collections import deque
from decimal import Decimal
import requests
from bs4 import BeautifulSoup
from django.conf import settings
from common.currency import symbol_to_currency


def get_price(url: str) -> dict:
    # Test mode -> skip real scraping and return a random fake price
    if settings.SCRAPER_TEST_MODE:
        price_random = random.randint(10, 50)
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

        raw_text = price_tag.get_text(strip=True)
        deque_text = deque(raw_text)
        currency_symbol = deque_text.popleft()
        currency = symbol_to_currency(currency_symbol)

        price = Decimal(''.join(deque_text).replace(',', '.'))

        if currency:
            result['currency'] = str(currency)
        if price:
            result['price'] = price

    return result

class StoreScraper:
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

class KateoStoreScraper(StoreScraper):
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

class BookToScrapeScraper:
    @staticmethod
    def get_product_info(url: str) -> dict:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        result = {}
        price_tag = soup.select_one('p.price_color:-soup-contains("£")')

        if price_tag:
            raw_text = price_tag.get_text(strip=True)

            if not raw_text:
                return result

            deque_text = deque(raw_text)
            hidden_symbol = deque_text.popleft()
            currency_symbol = deque_text.popleft()
            currency = symbol_to_currency(currency_symbol)

            price = Decimal(''.join(deque_text))

            if currency:
                result['currency'] = str(currency)
            if price:
                result['price'] = price

        title_tag = soup.find('div', class_='col-sm-6 product_main')
        if title_tag:
            title_tag = title_tag.find('h1')
            title = title_tag.get_text(strip=True)

            if title:
                result['title'] = title

        p_tags = soup.find_all('p')
        for p_tag in p_tags:
            description_tag = p_tag.find_previous('div', id='product_description')
            if description_tag:
                description = p_tag.get_text(strip=True)
                result['description'] = description
                break

        return result


def get_pattern(store: str) -> str:
    pattern = {
        'Kateo': r'https:\/\/kateo\.bg\/products\/[a-z0-9-]+\/?\?variant=\d{14}',
        'Books to Scrape': r"^https://books\.toscrape\.com/catalogue/[a-z][a-z0-9-]*_\d{3,}/index\.html$",
    }

    return pattern[store]


def dispatch_store(url: str, store: str) -> dict:
    info = {}

    if store == 'Kateo':
        info = KateoStoreScraper.get_product_info(url)
    elif store == 'Books to Scrape':
        info = BookToScrapeScraper.get_product_info(url)

    return info