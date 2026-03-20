from django.db import models

from common.mixins import CreatedAtMixin, BaseInfoTitle


# Create your models here.

class Store(CreatedAtMixin, BaseInfoTitle):
    url = models.URLField()
