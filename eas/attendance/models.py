from django.db import models

from django.utils import timezone
from employees.models import CustomUser


class Attendance(models.Model):
    karyawan = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="attendances")
    tanggal = models.DateField(default=timezone.localdate)
    jam_masuk = models.TimeField(null=True, blank=True)
    jam_keluar = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = ('karyawan', 'tanggal')

    def __str__(self):
        return f"{self.karyawan.nama} - {self.tanggal}"
