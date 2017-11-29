from django.contrib.auth.decorators import login_required, permission_required
from django.conf.urls import url
from .views import OrdenCreate, OrdenCerrar, OrdenCancelar, OrdenesList, OrdenDelete, OrdenDetail, ClienteListado,EquipoCreate, EquipoList, EquipoDelete,EquipoCreatePopUp,EquipoListado, EquipoCreateJson

urlpatterns = [
    url(r'^crear$', login_required(OrdenCreate.as_view(), login_url='usuario:login'), name="orden_crear"),
    url(r'^cerrar$', login_required(OrdenCerrar.as_view(), login_url='usuario:login'), name="orden_cerrar"),
    url(r'^cancelar$', login_required(OrdenCancelar.as_view(), login_url='usuario:login'), name="orden_cancelar"),
    url(r'^listar$', login_required(OrdenesList.as_view(), login_url='usuario:login'), name="orden_listar"),
    url(r'^eliminar/(?P<pk>\d+)$', login_required(OrdenDelete.as_view(), login_url='usuario:login'), name="orden_eliminar"),
    url(r'^ver/(?P<pk>\d+)$', login_required(OrdenDetail.as_view(), login_url='usuario:login'), name="orden_ver"),
    url(r'^lista_clientes$', login_required(ClienteListado.as_view(), login_url='usuario:login'), name="cliente_listar"),
    url(r'^lista_equipos$', login_required(EquipoListado.as_view(), login_url='usuario:login'), name="equipo_listar"),
    url(r'^equipo/crear$', login_required(EquipoCreate.as_view(), login_url='usuario:login'),name='equipo_crear'),
    url(r'^equipo/listar$', login_required(EquipoList.as_view(), login_url='usuario:login'),name='equipo_listar'),
    url(r'^equipo/eliminar/(?P<pk>\d+)$', login_required(EquipoDelete.as_view(), login_url='usuario:login'),name='equipo_eliminar'),
    url(r'^equipo/ver/(?P<pk>\d+)$', login_required(EquipoList.as_view(), login_url='usuario:login'), name='equipo_ver'),
    url(r'^equipo/editar/(?P<pk>\d+)$', login_required(EquipoList.as_view(), login_url='usuario:login'), name='equipo_editar'),
    url(r'^equipo/crear_popup/(?P<pk>\d+)$', login_required(EquipoCreatePopUp.as_view(), login_url='usuario:login'), name='equipo_crear_popup'),
    url(r'^equipo/crear_json', login_required(EquipoCreateJson.as_view(), login_url='usuario:login'), name='equipo_crear_json')
]

