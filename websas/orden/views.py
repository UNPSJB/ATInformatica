from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from django.template.loader import render_to_string

from django.http import JsonResponse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from servicio.models import TipoServicio
from .models import Orden, Equipo
from persona.models import Cliente, Tecnico, Persona
from rubro.models import Rubro

from .forms import OrdenForm, EquipoForm
# Create your views here.

class OrdenCreate(CreateView):
    model = Orden
    template_name = 'orden/orden_nueva.html'
    form_class = OrdenForm
    success_url = reverse_lazy('/')

    def get_context_data(self, **kwargs):
        # Llamar a super para recuperar el contexto original
        contexto = super(OrdenCreate, self).get_context_data(**kwargs)
        # Agregar lo que necesita la vista
        # contexto['clientes'] = Cliente.objects.all()
        contexto['rubros'] = Rubro.objects.all()
        contexto['tecnicos'] = Tecnico.objects.all()
        contexto['servicios'] = TipoServicio.objects.all()
        return contexto

    def post(self, request, *args, **kwargs):
        persona = Persona.objects.get(pk=request.POST.get('cliente'))
        rubro = Rubro.objects.get(pk=request.POST.get('rubro'))
        servicio = TipoServicio.objects.get(pk=request.POST.get('servicio'))

        print(persona, rubro, servicio)
        
        if persona.sos(Cliente):
            orden = Orden(usuario=request.user, cliente=persona.como(Cliente), rubro=rubro, tipo_servicio=servicio, descripcion="Alto bolonqui")
            orden.save()

            print(orden)

            return JsonResponse({'data':'Todo pioooola'})

        return JsonResponse({'data':'Todo mall'})
        
class OrdenesList(ListView):
    model = Orden
    template_name = 'orden/ordenes.html'

class OrdenDelete(DeleteView):
    model = Orden
    template_name = 'orden/orden_delete.html'
    success_url = reverse_lazy('orden:orden_listar')

class OrdenDetail(DetailView):
    model = Orden
    template_name = 'orden/orden_ver.html'
    
class ClienteListado(ListView):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'data':render_to_string('orden/listado_clientes.html',{'clientes':Cliente.objects.all()})})

class EquipoListado(ListView):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'data':render_to_string('orden/listado_equipos.html',{'equipos':Equipo.objects.all()})})

class EquipoCreate(CreateView):
    model = Equipo
    template_name = 'equipo/equipo_form.html'
    form_class = EquipoForm
    success_url = reverse_lazy('orden:equipo_listar')

class EquipoList(ListView):
    model = Equipo
    template_name = 'equipo/equipos.html'

class EquipoUpdate(UpdateView):
    model = Equipo
    template_name = 'equipo/equipo_form.html'
    form_class = EquipoForm
    success_url = reverse_lazy('orden:equipo_listar')
class EquipoDelete(DeleteView):
    model = Equipo
    template_name = 'equipo/equipo_delete.html'
    success_url = reverse_lazy('orden:equipo_listar')

class EquipoCreatePopUp(EquipoCreate):
    template_name ='equipo/equipo_form_popup.html'
    success_url = '#'
