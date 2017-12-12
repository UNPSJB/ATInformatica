from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import ReporteTotalOrdenes, ReporteCantidadOrdenes, ReporteProducto, ReporteEvolucionFacturacionMensual, ReporteCargaTrabajoTecnico
urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.

    url(r'^total_facturado/', login_required(ReporteTotalOrdenes.as_view(), login_url='usuario:login'), name="reportes"),
    url(r'^cantidad_ordenes/', login_required(ReporteCantidadOrdenes.as_view(), login_url='usuario:login'), name="cantidad_ordenes"),
    url(r'^productos/', login_required(ReporteProducto.as_view(), login_url='usuario:login'), name="productos"),
    url(r'^facturacion_mensual/', login_required(ReporteEvolucionFacturacionMensual.as_view(), login_url='usuario:login'), name="facturacion_mensual"),
    url(r'^carga_trabajo/', login_required(ReporteCargaTrabajoTecnico.as_view(), login_url='usuario:login'), name="carga_trabajo"),
]
