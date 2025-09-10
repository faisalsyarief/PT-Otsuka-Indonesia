from django.contrib import admin

# Register your models here.

from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('karyawan', 'tanggal', 'jam_masuk', 'jam_keluar')
    list_filter = ('tanggal', 'karyawan')
    search_fields = ('karyawan__nama', 'karyawan__email')