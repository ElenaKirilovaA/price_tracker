from decimal import Decimal
import random
from collections import deque
import requests
from bs4 import BeautifulSoup
from common.currency import symbol_to_currency
from abc import ABC, abstractmethod


def get_mock_data() -> Decimal:
    """
    The aim of this functon is to test celery functionality.
    :return: dict with mocked data for SCRAPER_TEST_MODE only.
    """
    price_random = random.randint(10, 150)
    price = Decimal(str(price_random))
    return price


class BaseScraper(ABC):
    headers = {'User-Agent': 'Mozilla/5.0'}

    def get_soup(self, url: str) -> BeautifulSoup:
        res = requests.get(url, headers=self.headers, timeout=8)
        return BeautifulSoup(res.text, 'html.parser')

    def scrape(self, url: str) -> dict:  # when create product from form
        soup = self.get_soup(url)

        result = {}
        result.update(self.get_price(soup) or {})
        result.update(self.get_title(soup) or {})
        result.update(self.get_description(soup) or {})

        return result

    def get_price_only(self, url: str) -> dict:  # when use Celery
        soup = self.get_soup(url)
        return self.get_price(soup)

    def get_price(self, soup: BeautifulSoup) -> dict:

        raw_text = self.get_price_text(soup)
        if not raw_text:
            return {}

        return self.parse_price(raw_text)

    def parse_price(self, raw_text: str) -> dict:
        deque_text = deque(raw_text)
        deque_text.popleft()  # hidden_symbol
        currency_symbol = deque_text.popleft()
        currency = symbol_to_currency(currency_symbol)
        price = Decimal(''.join(deque_text))

        return {'price': price, 'currency': str(currency)}

    @abstractmethod
    def get_price_text(self, soup: BeautifulSoup) -> str:
        pass

    @abstractmethod
    def get_title(self, soup: BeautifulSoup) -> dict:
        pass

    @abstractmethod
    def get_description(self, soup: BeautifulSoup) -> dict:
        pass


class KateoStoreScraper(BaseScraper):

    def parse_price(self, raw_text):
        deque_text = deque(raw_text)
        currency_symbol = deque_text.popleft()
        currency = symbol_to_currency(currency_symbol)
        price = Decimal(''.join(deque_text).replace(',', '.'))

        return {'price': price, 'currency': str(currency)}

    def get_price_text(self, soup: BeautifulSoup):
        price_tag = soup.select_one('span.price:-soup-contains("€")')

        return price_tag.get_text(strip=True) if price_tag else None

    def get_title(self, soup):
        title_tag = soup.find('h1')

        return {'title': title_tag.get_text(strip=True)[:100]} if title_tag else {}

    def get_description(self, soup):
        result = {}
        description = soup.find('rte-formatter')
        if description:
            p_description = description.find_next('p')
            if p_description:
                result['description'] = p_description.get_text(strip=True)

        return result


class BookToScrapeScraper(BaseScraper):

    def get_price_text(self, soup: BeautifulSoup) -> str:
        price_tag = soup.select_one('p.price_color:-soup-contains("£")')

        return price_tag.get_text(strip=True) if price_tag else None

    def get_title(self, soup: BeautifulSoup):
        title_tag = soup.find('div', class_='col-sm-6 product_main')
        if title_tag:
            title_tag = title_tag.find('h1')

        return {'title': title_tag.get_text(strip=True)[:100]} if title_tag else {}

    def get_description(self, soup: BeautifulSoup):
        p_tags = soup.find_all('p')
        for p_tag in p_tags:
            description_tag = p_tag.find_previous('div', id='product_description')
            if description_tag:
                return {'description':  p_tag.get_text(strip=True)}
        return {}


def get_pattern(store: str) -> str:
    pattern = {
        'Kateo': r'https:\/\/kateo\.bg\/products\/[a-z0-9-]+\/?\?variant=\d{14}',
        'Books to Scrape': r"^https://books\.toscrape\.com/catalogue/[a-z][a-z0-9-]*_\d{3,}/index\.html$",
    }

    return pattern[store]


def dispatch_store(store: str) -> BaseScraper or dict:
    stores = {
        'Kateo': KateoStoreScraper,
        'Books to Scrape': BookToScrapeScraper,
    }
    scraper_class = stores.get(store)

    if not scraper_class:
        return {}

    store_scraper = scraper_class()

    return store_scraper
