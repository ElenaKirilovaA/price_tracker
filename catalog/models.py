from cloudinary.models import CloudinaryField
from django.db import models
from common.mixins import CreatedAtMixin, BaseInfoTitle, BaseInfoDescription


# Create your models here.


class Category(CreatedAtMixin, BaseInfoTitle, BaseInfoDescription):
    card_image = CloudinaryField(
        'image',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.title


class Tag(CreatedAtMixin, BaseInfoTitle):

    def __str__(self):
        return self.title
