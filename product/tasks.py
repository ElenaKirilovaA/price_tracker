from celery import shared_task
from alert.tasks import check_alerts
from product.models import Product
from product.services import get_price


@shared_task
def check_price():
    products =  Product.objects.prefetch_related('alerts').filter(alerts__is_active=True)

    for product in products:
        old_price = product.current_price
        new_price = get_price(product.url)['price']

        if not new_price:
            return

        if old_price != new_price:
            product.current_price = new_price
            product.save()
            check_alerts.delay(product.id)
