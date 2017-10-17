from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from persona.views.cliente import ClienteCreate, ClienteCreatePopup, ClienteList, ClienteListJSON, ClienteUpdate, ClienteDelete, ClienteDetail

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.

    # The home page
    url(r'^listar$', login_required(ClienteList.as_view(), login_url='usuario:login'), name='cliente_listar'),
    url(r'^lista_json$', login_required(ClienteListJSON.as_view(), login_url='usuario:login'), name='cliente_listar_json'),
    url(r'^crear$', login_required(ClienteCreate.as_view(), login_url='usuario:login'), name='cliente_crear'),
    url(r'^crear_popup$', login_required(ClienteCreatePopup.as_view(), login_url='usuario:login'), name='cliente_crear_popup'),
    url(r'^editar/(?P<pk>\d+)$', login_required(ClienteUpdate.as_view(), login_url='usuario:login'), name='cliente_editar'),
    url(r'^eliminar/(?P<pk>\d+)$', login_required(ClienteDelete.as_view(), login_url='usuario:login'), name='cliente_eliminar'),
    url(r'^ver/(?P<pk>\d+)$', login_required(ClienteDetail.as_view(), login_url='usuario:login'), name='cliente_ver'),
    # url(r'^(?P<pk>\d+)$', views.cliente_detail, name='cliente_detail')
]