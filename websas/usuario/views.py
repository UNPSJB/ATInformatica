from django.shortcuts import render, redirect
from .forms import UsuarioUpdateForm, RegistrarUsuarioForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import Usuario
from persona.models import Persona, Rol
from django.views.generic import CreateView, UpdateView

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters


from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView, TemplateView, RedirectView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView

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
            self.success_url = reverse_lazy('usuario:password_change')
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    url = '/usuario/login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

class CambiarContraseñaView(PasswordChangeView):
    success_url = reverse_lazy('index:index')
    template_name = 'password_change_form.html'