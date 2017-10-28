from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from .views import OrdenCreate, OrdenesList, OrdenDelete, OrdenDetail

urlpatterns = [
    url(r'^crear$', OrdenCreate.as_view(), name="orden_crear"),
    url(r'^listar$', OrdenesList.as_view(), name="orden_listar"),
    url(r'^eliminar/(?P<pk>\d+)$', OrdenDelete.as_view(), name="orden_eliminar"),
    url(r'^ver/(?P<pk>\d+)$', OrdenDetail.as_view(), name="orden_ver"),
]

