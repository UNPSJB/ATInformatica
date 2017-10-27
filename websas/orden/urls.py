from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from .views import OrdenCreate,ClienteListado

urlpatterns = [
    url(r'^crear$', OrdenCreate.as_view(), name="orden_crear"),
    url(r'^lista_clientes$', ClienteListado.as_view(), name="cliente_listar"),
]

