from django.contrib import admin

from alert.models import Alert, ArchiveAlert


# Register your models here.
@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['id', 'started_price', 'email',]
    list_filter = ['is_active', 'product__title', 'product__category']
    search_fields = ['id', 'product__title', 'email']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'started_price']


@admin.register(ArchiveAlert)
class ArchiveAlertAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_title', 'started_price', 'target', 'triggered_price', 'category_title']
    list_filter = ['id', 'started_price_eur', 'triggered_price_eur']
    search_fields = ['product_title','started_price_eur', 'triggered_price_eur', 'category_title']
    ordering = ['-alert_finished_at']
    readonly_fields = ['alert_created_at', 'alert_finished_at']
