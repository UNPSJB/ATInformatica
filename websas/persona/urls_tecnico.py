from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from . import views
from .views import EmpleadoCreate, EmpleadoUpdate, EmpleadoDelete, EmpleadoDetail, TecnicoList, JefeTallerList, GerenteList

urlpatterns = [
    url(r'^listar/tecnico$', login_required(TecnicoList.as_view(), login_url='usuario:login'), name='tecnico_listar'),
    url(r'^listar/jefe$', login_required(JefeTallerList.as_view(), login_url='usuario:login'), name='jefe_listar'),
    url(r'^listar/gerente$', login_required(GerenteList.as_view(), login_url='usuario:login'), name='gerente_listar'),        
    url(r'^crear$', login_required(EmpleadoCreate.as_view(), login_url='usuario:login'), name='tecnico_crear'),
    url(r'^editar/(?P<pk>\d+)$', login_required(EmpleadoUpdate.as_view(), login_url='usuario:login'), name='tecnico_editar'),
    url(r'^eliminar/(?P<pk>\d+)$', login_required(EmpleadoDelete.as_view(), login_url='usuario:login'), name='tecnico_eliminar'),
    url(r'^ver/(?P<pk>\d+)$', login_required(EmpleadoDetail.as_view(), login_url='usuario:login'), name='tecnico_ver'),    
]