
from django.core.mail import EmailMessage
from django.conf import settings
from django.db import transaction
from django.db.models import F

from alert.models import ArchiveAlert, Alert, PriceTimeline, PriceTimelineArchived
from common.currency import convert_to_eur


def set_timeline_checks(alert: Alert) -> None:
    alert.counter_checks += 1
    alert.save()

    PriceTimeline.objects.create(
        alert=alert,
        price=alert.product.current_price
    )



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
    category = alert.product.category

    archive = ArchiveAlert.objects.create(
        product_title=product.title,
        started_price = alert.started_price,
        target = alert.target_price,
        product_currency = product.currency,
        started_price_eur = convert_to_eur(alert.started_price, product.currency),
        triggered_price_eur = convert_to_eur(alert.triggered_price, product.currency),
        triggered_price = alert.triggered_price,
        alert_created_at = alert.created_at,
        counter_checks = alert.counter_checks,
        category_title= category.title,
        category= category,
    )

    price_timelines = alert.price_timelines.all()  # TODO or list()?
    timeline_to_archive = [PriceTimelineArchived(
            history_alert=archive,
            price=timeline.price,
            checked_at=timeline.checked_at
        ) for timeline in price_timelines]

    PriceTimelineArchived.objects.bulk_create(timeline_to_archive)

    alert.delete()


def manage_simulation_tracking(alert: Alert) -> None:
    send_mail(alert)
    alert.is_active = False
    alert.save()
    archive_alert(alert)













