from celery import shared_task
from alert.models import Alert
from alert.service import sending_mail, archive_alert, set_timeline_checks


@shared_task
def manage_simulation_tracking(alert_id: int) -> None:
    alert = Alert.objects.get(id=alert_id)
    sending_mail(alert)
    alert.is_active = False
    alert.save()
    archive_alert(alert)


@shared_task
def check_alerts(product_id: int) -> None:
    alerts = Alert.objects.filter(product_id=product_id)

    for alert in alerts:
        set_timeline_checks(alert)

        if alert.price_is_dropped:
            manage_simulation_tracking.delay(alert.id)
