from django.contrib import admin

from catalog.models import Category, Tag


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    list_filter = ['title']
    search_fields = ['title', 'products__title']
    ordering = ['-title']
    readonly_fields = ['created_at']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title']
    list_filter = ['title']
    search_fields = ['title', 'products__title']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
