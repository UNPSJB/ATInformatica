from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from .views import UserAddGroup, GroupAddPermission,  RegistrarUsuario, GroupView, LoginView, LogoutView, CambiarContraseñaView, CambiarContraseñaOKView
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
)

urlpatterns = [
    url(r'login$', LoginView.as_view(), name="login"),
    url(r'logout$', login_required(LogoutView.as_view(), login_url='usuario:login'), name="logout"),
    url(r'crear$', login_required(RegistrarUsuario.as_view(), login_url='usuario:login'), name="usuario_crear"),
    url(r'grupos$', login_required(GroupView.as_view(), login_url='usuario:login'), name="grupos"),
    url(r'add_grupo$', login_required(UserAddGroup.as_view(), login_url='usuario:login'), name="usuario_add_grupo"),
    url(r'add_permiso$', login_required(GroupAddPermission.as_view(), login_url='usuario:login'), name="grupo_add_permiso"),
    url(r'^password_change/$', login_required(CambiarContraseñaView.as_view(), login_url='usuario:login'), name='password_change'),
    url(r'^password_change/done/$', login_required(CambiarContraseñaOKView.as_view(), login_url='usuario:login'), name='password_change_done'),
]
