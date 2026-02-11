from django.db import models
from django.db.models import F, ExpressionWrapper, DecimalField


class AlertManager(models.Manager):
    def get_active_alerts(self):
        return (self.select_related('product')
                .filter(
                    is_active=True)
                .order_by('-created_at', 'product__title'))


class ArchiveAlertManager(models.Manager):
    def get_archives_by_saved_money(self):
        return self.annotate(
        saved_money_db=ExpressionWrapper(
            F('started_price_eur') - F('triggered_price_eur'),
            output_field=DecimalField(max_digits=10, decimal_places=2))).order_by('-saved_money_db')
