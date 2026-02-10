from django.contrib import admin

from alert.models import Alert


# Register your models here.
@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    pass