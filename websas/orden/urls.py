from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from .views import orden_create

urlpatterns = [
    url(r'^crear$', orden_create, name="orden_crear"),
]

