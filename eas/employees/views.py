from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser
from .serializers import EmployeeSerializer
from .permissions import IsAdminOrReadSelf

from eas.mixins import StandardizedDestroyMixin

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import action

from rest_framework.response import Response
from django.http import HttpResponse

import pandas as pd


class EmployeeViewSet(StandardizedDestroyMixin, viewsets.ModelViewSet):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadSelf]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nama', 'status_aktif']
    
    search_fields = ["username", "email", "nama"]
    ordering_fields = ["id", "tanggal_masuk", "nama"]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return CustomUser.objects.all().order_by("id")
        return CustomUser.objects.filter(pk=user.pk)
    
    
    @action(detail=False, methods=['get'], url_path='export')
    def export_data(self, request):
        fmt = request.query_params.get('formatx', 'pdf')

        user = request.user
        if not (user.is_staff or user.is_superuser):
            return Response({"rc":403,"message":"Anda tidak punya akses","data":None}, status=403)

        employees = CustomUser.objects.all()
        data = []
        for e in employees:
            data.append({
                "Nama": e.nama,
                "Email": e.email,
                "Jabatan": e.jabatan,
                "Tanggal Masuk": e.tanggal_masuk,
                "Status Aktif": e.status_aktif,
            })

        df = pd.DataFrame(data)

        if fmt == 'excel':
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=employees.xlsx'
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
            return HttpResponse(buffer, content_type='application/pdf', headers={'Content-Disposition':'attachment; filename="employees.pdf"'})
        else:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=employees.csv'
            df.to_csv(response, index=False)
            return response
