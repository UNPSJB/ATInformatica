from django.conf.urls import url
from .views import login_user, logout_user, registrarUsuario

urlpatterns = [
    url(r'login$', login_user, name="login"),
    url(r'logout$', logout_user, name="logout"),
    url(r'crear/(?P<pk>\d+)$', registrarUsuario, name="usuario_crear"),
]
