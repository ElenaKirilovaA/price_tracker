from django.db import transaction
from django.core.mail import EmailMessage
from django.conf import settings

from alert.models import ArchiveAlert, Alert


def calculate_simulation_checks(alert: Alert) -> None:
    alert.counter_checks += 1
    alert.save()


def send_mail(alert: Alert) -> None:
    EmailMessage(
        subject=f'Price dropped for {alert.product.title}!',
        body=f'{alert}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[alert.email],
    ).send()


@transaction.atomic
def archive_alert(alert: Alert) -> None:

    if alert.started_price is None or alert.triggered_price is None:
        raise ValueError("ArchiveAlert can not be without started_price and/or triggered_price.")

    product = alert.product
    category = alert.product.category or None

    ArchiveAlert.objects.create(
        product_title=product.title,
        started_price = alert.started_price,
        target = alert.target_price,
        product_currency = product.currency,
        triggered_price = alert.triggered_price,
        alert_created_at = alert.created_at,
        counter_checks = alert.counter_checks,
        category_title= category,
        category= category,
    )
    alert.delete()


def manage_simulation_tracking(alert: Alert) -> None:
    send_mail(alert)
    alert.is_active = False
    alert.save()
    archive_alert(alert)













