from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from .views import TipoServicioCreate, TipoServicioList, TipoServicioUpdate, TipoServicioDelete

urlpatterns = [
    url(r'^crear$', login_required(TipoServicioCreate.as_view(), login_url='usuario:login', redirect_field_name=None, ), name="servicio_crear"),
    url(r'^listar$', login_required(TipoServicioList.as_view(), login_url='usuario:login'), name="servicio_listar"),
    url(r'^editar/(?P<pk>\d+)$', login_required(TipoServicioUpdate.as_view(), login_url='usuario:login'), name="servicio_editar"),
    url(r'^eliminar/(?P<pk>\d+)$', login_required(TipoServicioDelete.as_view(), login_url='usuario:login'), name="servicio_eliminar"),
    
]
