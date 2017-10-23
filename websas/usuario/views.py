from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .forms import UsuarioUpdateForm, RegistrarUsuarioForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import Usuario
from persona.models import Persona, Rol
from django.views.generic import View, CreateView, UpdateView

class RegistrarUsuario(CreateView):
    model = Usuario
    template_name = 'usuario_crear.html'
    form_class = RegistrarUsuarioForm
    success_url = reverse_lazy('cliente:cliente_listar')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        
        form = self.form_class(request.POST)
        if form.is_valid():
            usuario = form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)  
        return self.render_to_response(self.get_context_data(**kwargs))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        rol = Rol.objects.get(pk=pk)
        form = RegistrarUsuarioForm
        context['form'] = form
        context['persona'] = rol.persona
        return context

    """
    def get(self, request, *args, **kwargs):
        
        pk = self.kwargs.get('pk', 0)
        persona = Persona.objects.get(pk=pk)
        user = Usuario.objects.create_user(username=persona.doc,password=persona.doc, persona=persona)
        return HttpResponseRedirect(reverse_lazy('cliente:cliente_listar'))
    """

class UsuarioUpdate(UpdateView):
    model = Usuario
    template_name = 'usuario_editar.html'
    form_class = UsuarioUpdateForm
    success_url = reverse_lazy('cliente:cliente_listar')


@csrf_protect
def login_user(request):
    if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.primer_login and not user.is_superuser:
                    return HttpResponseRedirect(reverse_lazy('usuario:usuario_editar',kwargs={'pk':user.id}))
            return HttpResponseRedirect(reverse_lazy('index:index'))
    else: 
        return render(request, 'login.html')


@login_required(login_url='usuario:login')
def logout_user(request):
    logout(request)
    return redirect('/')