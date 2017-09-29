from django.conf.urls import url
from .views import login_user, logout_user, RegistrarUsuario, UsuarioUpdate

urlpatterns = [
    url(r'login$', login_user, name="login"),
    url(r'logout$', logout_user, name="logout"),
    url(r'crear/(?P<pk>\d+)$', RegistrarUsuario.as_view(), name="usuario_crear"),
    url(r'editar/(?P<pk>\d+)$', UsuarioUpdate.as_view(), name="usuario_editar"),
]
