from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from .views import TareaCreate
urlpatterns = [

    url(r'^crear/(?P<id_rubro>\d+)', login_required(TareaCreate.as_view(), login_url='usuario:login'), name='tarea_crear')
]