from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from persona.views.gerente import GerenteCreate, GerenteUpdate, GerenteList 
from persona.views.empleado import EmpleadoDelete, EmpleadoDetail

urlpatterns = [
    url(r'^listar$', login_required(GerenteList.as_view(), login_url='usuario:login'), name='gerente_listar'),        
    url(r'^crear$', login_required(GerenteCreate.as_view(), login_url='usuario:login'), name='gerente_crear'),
    url(r'^editar/(?P<pk>\d+)$', login_required(GerenteUpdate.as_view(), login_url='usuario:login'), name='gerente_editar'),
    url(r'^eliminar/(?P<pk>\d+)$', login_required(EmpleadoDelete.as_view(), login_url='usuario:login'), name='gerente_eliminar'),
    url(r'^ver/(?P<pk>\d+)$', login_required(EmpleadoDetail.as_view(), login_url='usuario:login'), name='gerente_ver'),    
]