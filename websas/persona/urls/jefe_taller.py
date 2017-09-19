from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from persona.views.jefe_taller import JefeTallerCreate, JefeTallerUpdate, JefeTallerList 
from persona.views.empleado import EmpleadoDelete, EmpleadoDetail

urlpatterns = [
    url(r'^listar$', login_required(JefeTallerList.as_view(), login_url='usuario:login'), name='jefe_listar'),        
    url(r'^crear$', login_required(JefeTallerCreate.as_view(), login_url='usuario:login'), name='jefe_crear'),
    url(r'^editar/(?P<pk>\d+)$', login_required(JefeTallerUpdate.as_view(), login_url='usuario:login'), name='jefe_editar'),
    url(r'^eliminar/(?P<pk>\d+)$', login_required(EmpleadoDelete.as_view(), login_url='usuario:login'), name='jefe_eliminar'),
    url(r'^ver/(?P<pk>\d+)$', login_required(EmpleadoDetail.as_view(), login_url='usuario:login'), name='jefe_ver'),    
]