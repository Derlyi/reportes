from django.http import HttpResponse
from django.shortcuts import render
from django import forms
from orders.models import Order, OrderItem
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime

class ReportDateForm(forms.Form):
    start_date = forms.DateField(label='Fecha de inicio', widget=forms.SelectDateWidget)
    end_date = forms.DateField(label='Fecha de fin', widget=forms.SelectDateWidget)

def sales_report_view(request):
    if request.method == 'POST':
        form = ReportDateForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            orders = Order.objects.filter(created__range=[start_date, end_date])
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'
            p = canvas.Canvas(response, pagesize=letter)

            p.drawString(100, 750, f"Reporte de ventas desde {start_date} hasta {end_date}")
            p.drawString(100, 730, f"Generado el: {datetime.now().strftime('%Y-%m-%d')}")

            y = 700
            total_sales = 0
            for order in orders:
                order_items = OrderItem.objects.filter(order=order)
                for item in order_items:
                    line = f"Producto: {item.product.name}, Cantidad: {item.quantity}, Precio: {item.get_cost()}"
                    p.drawString(100, y, line)
                    y -= 20
                    total_sales += item.get_cost()

            p.drawString(100, y-20, f"Total de ventas: ${total_sales:.2f}")
            p.showPage()
            p.save()
            return response
    else:
        form = ReportDateForm()

    return render(request, 'admin/sales_report.html')
