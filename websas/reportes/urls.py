from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import ReporteTotalOrdenes, ReporteProducto
urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.

    url(r'^total_facturado/', login_required(ReporteTotalOrdenes.as_view(), login_url='usuario:login'), name="reportes"),
    url(r'^productos/', login_required(ReporteProducto.as_view(), login_url='usuario:login'), name="productos"),
]
