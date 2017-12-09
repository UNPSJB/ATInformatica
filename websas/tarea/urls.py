from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from .views import ReservaCreate, TareaCancelar, TareaFinalizar, ObservacionCreate, TareaAceptar, TareaCreate, TareaDetail, TipoTareaCreate, TipoTareaDelete, TipoTareaUpdate, TareaCambiarPrecio
urlpatterns = [
    url(r'^agregar$', login_required(TareaCreate.as_view(), login_url='usuario:login'), name='tarea_crear'),
    url(r'^cancelar$', login_required(TareaCancelar.as_view(), login_url='usuario:login'), name='tarea_cancelar'),
    url(r'^aceptar$', login_required(TareaAceptar.as_view(), login_url='usuario:login'), name='tarea_aceptar'),
    url(r'^finalizar$', login_required(TareaFinalizar.as_view(), login_url='usuario:login'), name='tarea_finalizar'),
    url(r'^detalle/(?P<pk>\d+)$', login_required(TareaDetail.as_view(), login_url='usuario:login'), name='tarea_ver'),
    url(r'^reservar$', login_required(ReservaCreate.as_view(), login_url='usuario:login'), name='reserva_crear'),
    url(r'^observar$', login_required(ObservacionCreate.as_view(), login_url='usuario:login'), name='observacion_crear'),
    url(r'^cambiar_precio$', login_required(TareaCambiarPrecio.as_view(), login_url='usuario:login'), name='cambiar_precio'),
]
