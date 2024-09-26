from django.contrib import admin
from django.urls import path
from django.shortcuts import render

# Vista para el reporte de ventas
def sales_report_view(request):
    return render(request, 'admin/sales_report.html')

class ReportAdminSite(admin.AdminSite):
    site_header = "Administración de Informes"
    site_title = "Panel de Informes"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('sales_report/', self.admin_view(sales_report_view), name='sales-report'),
        ]
        return custom_urls + urls

# Instancia del sitio de administración personalizado
report_admin_site = ReportAdminSite(name='report_admin')

# Registra el sitio de administración personalizado
admin.site.site_header = "Administración Estándar"