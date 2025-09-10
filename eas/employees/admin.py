from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ("id", "nama", "email", "jabatan", "status_aktif", "is_staff", "is_superuser")
    list_filter = ("status_aktif", "is_staff", "is_superuser")
    search_fields = ("nama", "email", "jabatan")


admin.site.register(CustomUser, CustomUserAdmin)
