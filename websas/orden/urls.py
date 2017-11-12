from django.contrib.auth.decorators import login_required, permission_required
from django.conf.urls import url
from .views import OrdenCreate, OrdenCerrar, OrdenesList, OrdenDelete, OrdenDetail, ClienteListado,EquipoCreate, EquipoList, EquipoDelete,EquipoCreatePopUp,EquipoListado

urlpatterns = [
    url(r'^crear$', OrdenCreate.as_view(), name="orden_crear"),
    url(r'^cerrar$', OrdenCerrar.as_view(), name="orden_cerrar"),
    url(r'^listar$', OrdenesList.as_view(), name="orden_listar"),
    url(r'^eliminar/(?P<pk>\d+)$', OrdenDelete.as_view(), name="orden_eliminar"),
    url(r'^ver/(?P<pk>\d+)$', OrdenDetail.as_view(), name="orden_ver"),
    url(r'^lista_clientes$', ClienteListado.as_view(), name="cliente_listar"),
    url(r'^lista_equipos$', EquipoListado.as_view(), name="equipo_listar"),
    url(r'^equipo/crear$',EquipoCreate.as_view(),name='equipo_crear'),
    url(r'^equipo/listar$',EquipoList.as_view(),name='equipo_listar'),
    url(r'^equipo/eliminar/(?P<pk>\d+)$',EquipoDelete.as_view(),name='equipo_eliminar'),
    url(r'^equipo/ver/(?P<pk>\d+)$',EquipoList.as_view(),name='equipo_ver'),
    url(r'^equipo/editar/(?P<pk>\d+)$',EquipoList.as_view(),name='equipo_editar'),
    url(r'^equipo/crear_popup$',EquipoCreatePopUp.as_view(),name='equipo_crear_popup')
]

