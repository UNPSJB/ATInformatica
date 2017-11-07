from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from .views import RubroCreate, RubroList, RubroUpdate, RubroDelete
from tarea.views import TareaCreate, TareaDetail, TipoTareaCreate, TipoTareaList, TipoTareaDelete, TipoTareaUpdate, TipoTareaDetail

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    url(r'^crear/', login_required(RubroCreate.as_view(), login_url='usuario:login'), name="rubro_crear"),
    url(r'^listar/', login_required(RubroList.as_view(), login_url='usuario:login'), name="rubro_listar"),    
    url(r'^editar/(?P<pk>\d+)$', login_required(RubroUpdate.as_view(), login_url='usuario:login'), name="rubro_editar"),
    url(r'^eliminar/(?P<pk>\d+)$', login_required(RubroDelete.as_view(), login_url='usuario:login'), name="rubro_eliminar"),
    #URLs de TipoTarea para el Rubro
    url(r'^tareas/(?P<pk_rubro>\d+)/crear$', TipoTareaCreate.as_view(), name='tipo_tarea_crear'),
    url(r'^tareas/(?P<pk_rubro>\d+)/listar$', TipoTareaList.as_view(), name='tipo_tarea_listar'),
    url(r'^tareas/(?P<pk_rubro>\d+)/tarifar/(?P<pk_tarea>\d+)$', TipoTareaUpdate.as_view(), name='tipo_tarea_tarifar'),
    url(r'^tareas/(?P<pk_rubro>\d+)/eliminar/(?P<pk>\d+)$', TipoTareaDelete.as_view(), name='tipo_tarea_eliminar'),
    url(r'^tareas/(?P<pk_rubro>\d+)/ver/(?P<pk_tarea>\d+)$', TipoTareaDetail.as_view(), name='tipo_tarea_ver')

]
