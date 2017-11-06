from django.shortcuts import render, redirect
from .forms import UsuarioUpdateForm, RegistrarUsuarioForm, UsuarioCambiarPasswordForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import Usuario
from persona.models import Persona, Rol
from django.views.generic import CreateView, UpdateView

import datetime

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters


from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView, TemplateView, RedirectView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView

class RegistrarUsuario(TemplateView):
    model = Usuario
    template_name = 'usuario_crear.html'
    
    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk', 0)
        persona = Persona.objects.get(pk=pk)
        user = Usuario.objects.crear_usuario(username=persona.doc,password=persona.doc, persona=persona)
        if user:
            persona.agregar_rol(Usuario())
            return HttpResponseRedirect(reverse_lazy('cliente:cliente_listar'))
        return HttpResponseRedirect(reverse_lazy('empleado:tecnico:tecnico_listar'))


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "login.html"
    success_url =  reverse_lazy('index:index')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated(): 
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = Usuario.objects.get(username=form.get_user())
        if user.primer_login and not user.is_superuser:
            messages.warning(self.request, 'Se recomienda cambiar la contraseña predeterminada.')
            self.success_url = reverse_lazy('usuario:password_change')
        else:
            if user.last_login is not None:
                messages.info(self.request, '<i class="fa fa-info-circle fa-lg"></i>&nbsp;&nbsp;¡Bienvenido al sistema! - Último login: ' + user.last_login.strftime('%d/%m/%Y a las %H:%M:%S (hora del servidor)'))
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    url = '/usuario/login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

class CambiarContraseñaView(PasswordChangeView):
    form_class = UsuarioCambiarPasswordForm
    success_url = reverse_lazy('usuario:password_change_done')
    template_name = 'password_change_form.html'


class CambiarContraseñaOKView(PasswordChangeDoneView):
    def get(request, self):
        volver_url = reverse_lazy('usuario:logout')
        messages.success(self, '<i class="fa fa-check-circle fa-lg"></i>&nbsp;&nbsp;La contraseña se actualizó correctamente. Vuelva a iniciar sesión, por favor.')
        return HttpResponseRedirect(volver_url)