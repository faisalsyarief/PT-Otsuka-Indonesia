from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.utils import timezone

from .models import Attendance
from .serializers import AttendanceSerializer
from .permissions import AttendancePermission

from eas.mixins import StandardizedDestroyMixin

from rest_framework.decorators import action
from rest_framework.response import Response

from django.http import HttpResponse

import pandas as pd


class AttendanceViewSet(StandardizedDestroyMixin, viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, AttendancePermission]


    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Attendance.objects.all().order_by('-tanggal')
        return Attendance.objects.filter(karyawan=user).order_by('-tanggal')


    def create(self, request, *args, **kwargs):
        user = request.user
        today = timezone.localdate()

        attendance, created = Attendance.objects.get_or_create(karyawan=user, tanggal=today)

        if attendance.jam_masuk is None:
            attendance.jam_masuk = timezone.localtime().time()
            attendance.save()
            return Response({"status": "check-in berhasil", "jam_masuk": attendance.jam_masuk})
        elif attendance.jam_keluar is None:
            attendance.jam_keluar = timezone.localtime().time()
            attendance.save()
            return Response({"status": "check-out berhasil", "jam_keluar": attendance.jam_keluar})
        else:
            return Response({"status": "absensi hari ini sudah lengkap"}, status=status.HTTP_400_BAD_REQUEST)



    @action(detail=False, methods=['get'], url_path='export')
    def export_data(self, request):
        fmt = request.query_params.get('format', 'pdf')
        
        user = request.user
        if not (user.is_staff or user.is_superuser):
            return Response({"rc":403,"message":"Anda tidak punya akses","data":None}, status=403)

        attendances = Attendance.objects.all()
        data = []
        for a in attendances:
            data.append({
                "Nama": a.karyawan.nama,
                "Email": a.karyawan.email,
                "Tanggal": a.tanggal,
                "Jam Masuk": a.jam_masuk,
                "Jam Keluar": a.jam_keluar
            })

        df = pd.DataFrame(data)

        if fmt == 'excel':
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=attendance.xlsx'
            df.to_excel(response, index=False)
            return response
        elif fmt == 'pdf':
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
            from reportlab.lib import colors
            from io import BytesIO
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer)
            table_data = [list(df.columns)] + df.values.tolist()
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
                ('ALIGN',(0,0),(-1,-1),'CENTER'),
                ('GRID', (0,0), (-1,-1), 1, colors.black),
            ]))
            doc.build([table])
            buffer.seek(0)
            return HttpResponse(buffer, content_type='application/pdf', headers={'Content-Disposition':'attachment; filename="attendance.pdf"'})
        else:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=attendance.csv'
            df.to_csv(response, index=False)
            return response
