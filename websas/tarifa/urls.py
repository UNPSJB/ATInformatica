from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from .views import TarifaCreate

urlpatterns = [
    url(r'^crear/', login_required(TarifaCreate.as_view(), login_url='usuario:login'), name='tarifa_crear')

]