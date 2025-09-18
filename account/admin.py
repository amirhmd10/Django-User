# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, Profile


class ProfileInline(admin.StackedInline):
    """
    نمایش و ویرایش پروفایل داخل صفحه‌ی User
    """
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fk_name = "user" #برای نشان دادن رابطه بین کلید خارجی
    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    مدیریت کامل کاربر سفارشی
    """
    model = User
    inlines = [ProfileInline]

    list_display = ("email", "username", "is_staff", "is_active", "is_superuser")
    list_filter = ("is_staff", "is_active", "is_superuser")
    search_fields = ("email", "username")
    ordering = ("email",)
    readonly_fields = ()

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        (_("Permissions"), {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        (_("Important dates"), {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    def get_inline_instances(self, request, obj=None):
        """نمایش اینلاین پروفایل فقط در صورتی که User موجود باشد"""
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    مدیریت جداگانه پروفایل (در کنار اینلاین)
    """
    model = Profile
    list_display = (
        "user",
        "first_name",
        "last_name",
        "phone_number",
        "is_verified",
        "date_joined",
        "last_activity",
    )
    list_filter = ("is_verified", "date_joined")
    search_fields = (
        "user__email",
        "user__username",
        "first_name",
        "last_name",
        "phone_number",
    )
    ordering = ("-date_joined",)
