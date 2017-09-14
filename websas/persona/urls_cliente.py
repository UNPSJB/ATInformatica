from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views
from .views import ClienteCreate, ClienteList, ClienteUpdate, ClienteDelete

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.

    # The home page
    url(r'^listar$', login_required(ClienteList.as_view(), login_url='usuario:login'), name='cliente_listar'),
    url(r'^crear$', login_required(ClienteCreate.as_view(), login_url='usuario:login'), name='cliente_crear'),
    url(r'^editar/(?P<pk>\d+)$', login_required(ClienteUpdate.as_view(), login_url='usuario:login'), name='cliente_editar'),
    url(r'^eliminar/(?P<pk>\d+)$', login_required(ClienteDelete.as_view(), login_url='usuario:login'), name='cliente_eliminar'),
    # url(r'^(?P<pk>\d+)$', views.cliente_detail, name='cliente_detail')
]