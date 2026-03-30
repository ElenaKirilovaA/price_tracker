from celery import shared_task
from alert.tasks import check_alerts
from product.models import Product
from product.services import BaseScraper, dispatch_store


@shared_task
def check_price():
    products =  Product.objects.prefetch_related('alerts').filter(alerts__is_active=True)

    for product in products:
        store_scraper: BaseScraper = dispatch_store(product.store.title)
        old_price = product.current_price
        new_price = store_scraper.get_price_only(product.url)['price']

        if not new_price:
            continue  # not return!!!!

        if old_price != new_price:
            product.current_price = new_price
            product.save()
            check_alerts.delay(product.id)
