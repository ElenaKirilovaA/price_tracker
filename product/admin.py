from django.contrib import admin

from product.models import Product


# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'current_price', 'currency', 'slug']
    list_filter = ['currency']
    search_fields = ['title','slug', 'description', 'url', 'alerts__is_active']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
