from django.contrib.admin.forms import AdminPasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from accounts.forms import AppUserCreationForm, AppUserChangeForm
from accounts.models import Profile

UserModel = get_user_model()
# Register your models here.
@admin.register(UserModel)
class AppUserAdmin(BaseUserAdmin):
    add_form_template = "admin/auth/user/add_form.html"
    change_user_password_template = None
    fieldsets = (
        (None, {"fields": ("password",)}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                # include email and password for custom user
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    form = AppUserChangeForm
    add_form = AppUserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ("email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("first_name", "last_name", "email")
    ordering = ('email',)



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass