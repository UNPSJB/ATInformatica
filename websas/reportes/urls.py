from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import ReporteTotalOrdenes, ReporteCantidadOrdenes, ReporteTotalProductos, ReporteCantidadProductos, ReporteEvolucionFacturacionMensual, ReporteCargaTrabajoTecnico, ReporteTareaMasRealizada, ReporteTecnicoFinalizador
urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.

    url(r'^total_facturado/', login_required(ReporteTotalOrdenes.as_view(), login_url='usuario:login'), name="reportes"),
    url(r'^cantidad_ordenes/', login_required(ReporteCantidadOrdenes.as_view(), login_url='usuario:login'), name="cantidad_ordenes"),
    url(r'^productos/', login_required(ReporteTotalProductos.as_view(), login_url='usuario:login'), name="productos"),
    url(r'^cantidad_productos/', login_required(ReporteCantidadProductos.as_view(), login_url='usuario:login'), name="cantidad_productos"),
    url(r'^facturacion_mensual/', login_required(ReporteEvolucionFacturacionMensual.as_view(), login_url='usuario:login'), name="facturacion_mensual"),
    url(r'^carga_trabajo/', login_required(ReporteCargaTrabajoTecnico.as_view(), login_url='usuario:login'), name="carga_trabajo"),
    url(r'^tarea_mas_realizada/', login_required(ReporteTareaMasRealizada.as_view(), login_url='usuario:login'), name="tarea_mas_realizada"),
    url(r'^tecnico_finalizador/', login_required(ReporteTecnicoFinalizador.as_view(), login_url='usuario:login'), name="tecnico_finalizador"),
    
]
