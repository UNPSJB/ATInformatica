from django.contrib.auth.decorators import login_required
from django.conf.urls import url

from . import views
from .views import TecnicoCreate, TecnicoList, TecnicoUpdate, TecnicoDelete

urlpatterns = [
    url(r'^listar$', login_required(TecnicoList.as_view(), login_url='usuario:login'), name='tecnico_listar'),
    url(r'^crear$', login_required(TecnicoCreate.as_view(), login_url='usuario:login'), name='tecnico_crear'),
    url(r'^editar/(?P<pk>\d+)$', login_required(TecnicoUpdate.as_view(), login_url='usuario:login'), name='tecnico_editar'),
    url(r'^eliminar/(?P<pk>\d+)$', login_required(TecnicoDelete.as_view(), login_url='usuario:login'), name='tecnico_eliminar'),
]