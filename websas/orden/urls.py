from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from .views import OrdenCreate

urlpatterns = [
    url(r'^crear$', OrdenCreate.as_view(), name="orden_crear"),
]

