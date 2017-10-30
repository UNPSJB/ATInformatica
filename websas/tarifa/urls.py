from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from .views import TarifaCreate, TarifaList, TarifaDelete, TarifaDetail, TarifaUpdate

urlpatterns = [
    url(r'^crear/', TarifaCreate.as_view(), name='tarifa_crear'),
    url(r'^listar$', TarifaList.as_view(), name='tarifa_listar'),
    url(r'^editar/(?P<pk>\d+)$', TarifaUpdate.as_view(), name='tarifa_editar'),
    url(r'^eliminar/(?P<pk>\d+)$$', TarifaDelete.as_view(), name='tarifa_eliminar'),
    url(r'^ver/(?P<pk>\d+)$$', TarifaDetail.as_view(), name='tarifa_ver')

]