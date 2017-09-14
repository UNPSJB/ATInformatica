from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from .views import ProductoCreate, ProductoList, ProductoDelete, ProductoUpdate 

urlpatterns = [
    url(r'^crear$', login_required(ProductoCreate.as_view(), login_url='usuario:login'), name="producto_crear"),
    url(r'^listar$', login_required(ProductoList.as_view(), login_url='usuario:login'), name="producto_listar"),
    url(r'^editar/(?P<pk>\d+)$', login_required(ProductoUpdate.as_view(), login_url='usuario:login'), name="producto_editar"),
    url(r'^eliminar/(?P<pk>\d+)$', login_required(ProductoDelete.as_view(), login_url='usuario:login'), name="producto_eliminar"),
]