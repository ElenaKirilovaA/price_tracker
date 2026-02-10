from django.contrib import admin

from catalog.models import Category, Tag


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass