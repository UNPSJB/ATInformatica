from django.conf.urls import url
from .views import TipoServicioCreate, TipoServicioList, TipoServicioUpdate, TipoServicioDelete

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    url(r'^crear$', TipoServicioCreate.as_view(), name="servicio_crear"),
    url(r'^listar$', TipoServicioList.as_view(), name="servicio_listar"),
    url(r'^editar/(?P<pk>\d+)$', TipoServicioUpdate.as_view(), name="servicio_editar"),
    url(r'^eliminar/(?P<pk>\d+)$', TipoServicioDelete.as_view(), name="servicio_eliminar"),
]
