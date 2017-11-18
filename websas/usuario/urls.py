from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from .views import RegistrarUsuario, GroupView, LoginView, LogoutView, CambiarContraseñaView, CambiarContraseñaOKView
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
)
urlpatterns = [
    url(r'login$', LoginView.as_view(), name="login"),
    url(r'logout$', login_required(LogoutView.as_view(), login_url='usuario:login'), name="logout"),
    url(r'crear$', RegistrarUsuario.as_view(), name="usuario_crear"),
    url(r'grupos$', GroupView.as_view(), name="grupos"),
    url(r'^password_change/$', CambiarContraseñaView.as_view(), name='password_change'),
    url(r'^password_change/done/$', CambiarContraseñaOKView.as_view(), name='password_change_done'),
]
