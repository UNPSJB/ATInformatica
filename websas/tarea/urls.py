from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from .views import ReservaCreate, TareaFinalizar, ObservacionCreate, TareaAceptar, TareaCreate, TareaDetail, TipoTareaCreate, TipoTareaDelete, TipoTareaUpdate
urlpatterns = [
    url(r'^agregar$', TareaCreate.as_view(), name='tarea_crear'),
    url(r'^aceptar$', TareaAceptar.as_view(), name='tarea_aceptar'),
    url(r'^finalizar$', TareaFinalizar.as_view(), name='tarea_finalizar'),
    url(r'^detalle/(?P<pk>\d+)$', TareaDetail.as_view(), name='tarea_ver'),
    url(r'^reservar$', ReservaCreate.as_view(), name='reserva_crear'),
    url(r'^observar$', ObservacionCreate.as_view(), name='observacion_crear'),
]