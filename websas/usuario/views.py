from .forms import registrarUsuarioFormFactory, UserAddGroupForm, GroupAddPermissionForm, UsuarioCambiarPasswordForm, CrearGrupoForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from .models import Usuario
from persona.models import Persona, Rol

import datetime

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters


from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, Permission
from django.views.generic import FormView, TemplateView, RedirectView, View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView

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
            return super(self.__class__, self).dispatch(request, *args, **kwargs)

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

class RegistrarUsuario(View):

    def post(self, request, *args, **kwargs):
        persona_id = request.POST['persona_id']
        form = registrarUsuarioFormFactory(persona_id)
        # import ipdb; ipdb.set_trace()
        if form.is_valid():
            form.save()
            return JsonResponse({'data':'joya', 'successurl':reverse_lazy('usuario:grupos')})

        response = JsonResponse({'data': form.errors})
        response.status_code = 403  
        return response

class CambiarContraseñaView(PasswordChangeView):
    form_class = UsuarioCambiarPasswordForm
    success_url = reverse_lazy('usuario:password_change_done')
    template_name = 'password_change_form.html'


class CambiarContraseñaOKView(PasswordChangeDoneView):
    def get(request, self):
        volver_url = reverse_lazy('usuario:logout')
        messages.success(self, '<i class="fa fa-check-circle fa-lg"></i>&nbsp;&nbsp;La contraseña se actualizó correctamente. Vuelva a iniciar sesión, por favor.')
        return HttpResponseRedirect(volver_url)

class GroupView(TemplateView):
    template_name = 'grupos.html'

    def post(self, request, *args, **kwargs):
        form = CrearGrupoForm(request.POST or None)
       
        if form.is_valid():
            form.save()
            return JsonResponse({'data':'todo piola'})

        response = JsonResponse({'error': 'se pudrió todo'})
        response.status_code = 403  
        return response


    def get_context_data(self, **kwargs):
        contexto = super(GroupView, self).get_context_data(**kwargs)
        contexto['grupos'] = Group.objects.all()
        contexto['permisos'] = Permission.objects.all()
        contexto['usuarios'] = Usuario.objects.all()
        return contexto

class UserAddGroup(View):

    def post(self, request, *args, **kwargs):
        
        form = UserAddGroupForm(request.POST or None)
        if form.is_valid():
            form.save()
            return JsonResponse({'data':'todo piola'})

        response = JsonResponse({'error': 'se pudrió todo'})
        response.status_code = 403  
        return response

class GroupAddPermission(View):

    def post(self, request, *args, **kwargs):

        form = GroupAddPermissionForm(request.POST or None)
        if form.is_valid():
            form.save()
            return JsonResponse({'data':'todo piola'})

        response = JsonResponse({'error': 'se pudrió todo'})
        response.status_code = 403  
        return response