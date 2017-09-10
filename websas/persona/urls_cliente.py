from django.conf.urls import url
from . import views
from .views import ClienteCreate, ClienteList, ClienteUpdate, ClienteDelete

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.

    # The home page
    url(r'^listar$', ClienteList.as_view(), name='cliente_listar'),
    url(r'^crear$', ClienteCreate.as_view(), name='cliente_crear'),
    url(r'^editar/(?P<pk>\d+)$', ClienteUpdate.as_view(), name='cliente_editar'),
    url(r'^eliminar/(?P<pk>\d+)$', ClienteDelete.as_view(), name='cliente_eliminar'),
    # url(r'^(?P<pk>\d+)$', views.cliente_detail, name='cliente_detail')
]