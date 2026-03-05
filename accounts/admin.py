from django.contrib import admin

from accounts.models import AppUser, Profile


# Register your models here.
@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass