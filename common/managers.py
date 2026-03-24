from django.db import models
from django.db.models import QuerySet,F, ExpressionWrapper, DecimalField

from alert.models import ArchiveAlert


class AppUserQuerySet(models.QuerySet):
    # def get_saved_money_per_user(self):
    #     archives = (
    #                 ArchiveAlert.objects
    #                 .filter(user=profile.user)
    #                 .aggregate(
    #                     saved_money_db=Sum(
    #                         ExpressionWrapper(
    #                             F('started_price_eur') - F('triggered_price_eur'),
    #                             output_field=DecimalField()
    #                         )
    #                     )
    #                 )
    #             )
    pass