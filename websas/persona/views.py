from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.template import loader
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.contenttypes.models import ContentType
from usuario.models import Usuario
from persona.models import Rol
import abc
from .models import Tecnico, JefeTaller, Gerente, Cliente, Persona
from .forms import PersonaForm, EmpleadoForm

"""""""""""""""""""""""""""""""""""""""
Vistas de clientes
"""""""""""""""""""""""""""""""""""""""
class ClienteList(ListView):
    model = Cliente
    template_name = 'persona/clientes.html'

    def get_queryset(self):
        return Persona.objects.filter(pk__in=Cliente.objects.all().values('persona'))

class ClienteCreate(CreateView):
    model = Persona
    template_name = 'persona/cliente_detail.html'
    form_class = PersonaForm
    success_url = reverse_lazy('cliente:cliente_listar')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            persona = form.save()
            cliente = Cliente(persona=persona)
            cliente.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class ClienteUpdate(UpdateView):
    model = Persona
    template_name = 'persona/cliente_detail.html'
    form_class = PersonaForm
    success_url = reverse_lazy('cliente:cliente_listar')

class ClienteDelete(DeleteView):
    model = Persona
    template_name = 'persona/cliente_delete.html'
    success_url = reverse_lazy('cliente:cliente_listar')

"""""""""""""""""""""""""""""""""""""""
Vistas de empleados
"""""""""""""""""""""""""""""""""""""""
class EmpleadoCreate(CreateView):
    model = Persona
    template_name = 'persona/tecnico_detail.html'
    form_class = EmpleadoForm
    success_url = reverse_lazy('tecnico:tecnico_listar')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            persona = form.save()
            rol = form.cleaned_data['rol']
            self.crear_rol(persona, rol)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))
    
    def crear_rol(self, persona, rol):
        if rol == 'TC':
            tecnico = Tecnico(persona=persona)
            tecnico.save()
        elif rol == 'JT':
            jefe_taller = JefeTaller(persona=persona)
            jefe_taller.save()
        elif rol == 'G':   
            gerente = Gerente(persona=persona)
            gerente.save()

class EmpleadoUpdate(UpdateView):
    model = Persona
    template_name = 'persona/tecnico_detail.html'
    form_class = PersonaForm
    success_url = reverse_lazy('tecnico:tecnico_listar')

class EmpleadoDelete(DeleteView):
    model = Persona
    template_name = 'persona/tecnico_delete.html'
    success_url = reverse_lazy('tecnico:tecnico_listar')

class EmpleadoList(ListView):
    model = Persona
    template_name = 'persona/tecnicos.html'

class EmpleadoDetail(DetailView):
    model = Persona
    template_name = 'persona/tecnico_ver.html'

class TecnicoList(EmpleadoList):

    def get_queryset(self):
        return Persona.objects.filter(pk__in=Tecnico.objects.all().values('persona'))

class JefeTallerList(EmpleadoList):

    def get_queryset(self):
        return Persona.objects.filter(pk__in=JefeTaller.objects.all().values('persona'))

class GerenteList(EmpleadoList):

    def get_queryset(self):
        return Persona.objects.filter(pk__in=Gerente.objects.all().values('persona'))
