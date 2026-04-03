from django.core.validators import MinLengthValidator
from django.db import models


class BaseInfoTitle(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(
        unique=True,
        max_length=100,
        validators=[
            MinLengthValidator(2)
        ],
    )


class BaseInfoDescription(models.Model):
    class Meta:
        abstract = True

    description = models.TextField(
            blank=True,
            null=True
        )


class CreatedAtMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

class AppUserQuerysetMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class PageTitleMixin:
    page_title = None  # default value

    def get_page_title(self):
        return self.page_title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.get_page_title()
        return context
