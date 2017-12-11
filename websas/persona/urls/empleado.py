from django.contrib.auth.decorators import login_required
from django.conf.urls import url, include
from persona.views.empleado import EmpleadoCreate, EmpleadoEliminarRol, EmpleadoDelete, EmpleadoDetail, EmpleadoList, EmpleadoUpdate
urlpatterns = [
    # url(r'^tecnico/', include('persona.urls.tecnico', namespace="tecnico")),
    # url(r'^jefe/', include('persona.urls.jefe_taller', namespace="jefe")),
    # url(r'^Empleado/', include('persona.urls.Empleado', namespace="Empleado")),
    url(r'^listar$', login_required(EmpleadoList.as_view(), login_url='usuario:login'), name='empleado_listar'),        
    url(r'^crear$', login_required(EmpleadoCreate.as_view(), login_url='usuario:login'), name='empleado_crear'),
    url(r'^editar/(?P<pk>\d+)$', login_required(EmpleadoUpdate.as_view(), login_url='usuario:login'), name='empleado_editar'),
    url(r'^eliminar/(?P<pk>\d+)$', login_required(EmpleadoDelete.as_view(), login_url='usuario:login'), name='empleado_eliminar'),
    url(r'^ver/(?P<pk>\d+)$', login_required(EmpleadoDetail.as_view(), login_url='usuario:login'), name='empleado_ver'),    
    url(r'^eliminar-rol$', login_required(EmpleadoEliminarRol.as_view(), login_url='usuario:login'), name='empleado_eliminar_rol'),

]