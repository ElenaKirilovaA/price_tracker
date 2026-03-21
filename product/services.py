from decimal import Decimal

import requests
from bs4 import BeautifulSoup
# url = 'https://kateo.bg/products/glowwa-hair-food-vitamini-za-kosa-za-1-mesec?variant=55414409298306'

# class KateoStoreScraper:
def get_price(url) -> dict or None:

    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    result = {}
    price_tag = soup.find('span', class_='price')
    title_tag = soup.find('h1')
    description_formatter = soup.find('rte-formatter')


    if price_tag:
        _, price = price_tag.get_text(strip=True).split('€')
        price = price.replace(',', '.')
        price = price.strip()
        result['price'] = Decimal(price)

    if title_tag:
        result['title'] = title_tag.get_text(strip=True)[:100]

    if description_formatter:
        p_description = description_formatter.find_next('p')
        result['description'] = p_description.get_text(strip=True)

    return result
