from rest_framework import serializers
from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'karyawan', 'tanggal', 'jam_masuk', 'jam_keluar']
        read_only_fields = ['id', 'karyawan', 'tanggal', 'jam_masuk', 'jam_keluar']
