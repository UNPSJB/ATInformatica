from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from .views import TareaCreate, TipoTareaCreate, TipoTareaList, TipoTareaDelete, TipoTareaUpdate, TipoTareaDetail
urlpatterns = [
    url(r'^agregar$', TareaCreate.as_view(), name='tarea_crear'),
    #url(r'^crear/(?P<id_rubro>\d+)', login_required(TareaCreate.as_view(), login_url='usuario:login'), name='tarea_crear')
    url(r'^crear$', TipoTareaCreate.as_view(), name='tipo_tarea_crear'),
    url(r'^listar$', TipoTareaList.as_view(), name='tipo_tarea_listar'),
    url(r'^editar/(?P<pk>\d+)$', TipoTareaUpdate.as_view(), name='tipo_tarea_editar'),
    url(r'^eliminar/(?P<pk>\d+)$$', TipoTareaDelete.as_view(), name='tipo_tarea_eliminar'),
    url(r'^ver/(?P<pk>\d+)$$', TipoTareaDetail.as_view(), name='tipo_tarea_ver')
]