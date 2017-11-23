from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from .views import RubroCreate, RubroList, RubroUpdate, RubroDelete
from tarea.views import TareaCreate, TareaDetail, TipoTareaCreate, TipoTareaDelete, TipoTareaUpdate, TipoTareaTarifar

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    url(r'^crear/', login_required(RubroCreate.as_view(), login_url='usuario:login'), name="rubro_crear"),
    url(r'^listar/', login_required(RubroList.as_view(), login_url='usuario:login'), name="rubro_listar"),    
    url(r'^editar/(?P<pk>\d+)$', login_required(RubroUpdate.as_view(), login_url='usuario:login'), name="rubro_editar"),
    url(r'^eliminar/(?P<pk>\d+)$', login_required(RubroDelete.as_view(), login_url='usuario:login'),name="rubro_eliminar"),
    #URLs de TipoTarea para el Rubro
    url(r'^tareas/(?P<pk_rubro>\d+)/crear$', login_required(TipoTareaCreate.as_view(),login_url='usuario:login'), name='tipo_tarea_crear'),
    url(r'^tareas/(?P<pk_rubro>\d+)/editar/(?P<pk>\d+)$', login_required(TipoTareaUpdate.as_view(),login_url='usuario:login'), name='tipo_tarea_editar'),
    url(r'^tareas/(?P<pk_rubro>\d+)/tarifar/(?P<pk>\d+)$', login_required(TipoTareaTarifar.as_view(),login_url='usuario:login'), name='tipo_tarea_tarifar'),
    url(r'^tareas/(?P<pk_rubro>\d+)/eliminar/(?P<pk>\d+)$', login_required(TipoTareaDelete.as_view(),login_url='usuario:login'), name='tipo_tarea_eliminar'),
]
