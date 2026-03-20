from django.contrib import admin

from store.models import Store


# Register your models here.

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    pass