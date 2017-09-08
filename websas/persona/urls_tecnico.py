from django.conf.urls import url
from . import views
from .views import TecnicoCreate, TecnicoList, TecnicoUpdate, TecnicoDelete
urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.

    # The home page
    url(r'^listar$', TecnicoList.as_view(), name='tecnico_listar'),
    url(r'^crear$', TecnicoCreate.as_view(), name='tecnico_crear'),
    url(r'^editar/(?P<pk>\d+)$', TecnicoUpdate.as_view(), name='tecnico_editar'),
    url(r'^eliminar/(?P<pk>\d+)$', TecnicoDelete.as_view(), name='tecnico_eliminar'),
    #url(r'^(?P<pk>\d+)$', views.tecnico, name='tecnico_detail')
]