from django.db import models
from django.db.models import QuerySet,F, ExpressionWrapper, DecimalField



class ActiveAlertQuerySet(models.QuerySet):
    def get_active_alerts(self):
        return (self.select_related('product')
                .filter(is_active=True)
                .order_by('-created_at', 'product__title'))


class ArchiveAlertQuerySet(models.QuerySet):
    def get_archives_by_saved_money(self):
        return (self.annotate(saved_money_db=F('started_price_eur') - F('triggered_price_eur'))
                .order_by('-saved_money_db'))




