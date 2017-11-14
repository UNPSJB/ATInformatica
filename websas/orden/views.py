from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from django.template.loader import render_to_string

from django.http import JsonResponse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView, View
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
        contexto['rubros'] = Rubro.objects.all()
        contexto['tecnicos'] = Tecnico.objects.all()
        contexto['servicios'] = TipoServicio.objects.all()
        return contexto

    @method_decorator(permission_required('orden.add_orden', login_url='orden:orden_listar'))        
    def post(self, request, *args, **kwargs):
        persona = Persona.objects.get(pk=request.POST.get('cliente'))
        rubro = Rubro.objects.get(pk=request.POST.get('rubro'))
        servicio = TipoServicio.objects.get(pk=request.POST.get('servicio'))
        tecnico = Persona.objects.get(pk=request.POST.get('tecnico'))
        equipo = Equipo.objects.get(pk=request.POST.get('equipo'))
        descripcion = request.POST.get('observacion')
        print(persona, rubro, servicio,tecnico)
        
        if persona.sos(Cliente):
            orden = Orden(usuario=request.user, cliente=persona.como(Cliente), tecnico=tecnico.como(Tecnico), rubro=rubro, tipo_servicio=servicio, descripcion=descripcion,equipo=equipo) 
            orden.save()
            
            return JsonResponse({'data':'Todo pioooola'})

        return JsonResponse({'data':'Todo mall'})

class OrdenCerrar(View):

    @method_decorator(permission_required('orden.change_orden', login_url='orden:orden_listar'))
    def post(self, request, *args, **kwargs):
        orden = Orden.objects.get(pk=request.POST['orden_id'])
        if not orden:
            return JsonResponse({'error': 'no existe la orden de trabajo'})
        try:
            orden.cerrar()
        except Exception as e:
            response = JsonResponse({'error': str(e)})
            response.status_code = 403  
            return response
        return JsonResponse({'data':'ok'})

class OrdenCancelar(View):

    @method_decorator(permission_required('orden.change_orden', login_url='orden:orden_listar'))
    def post(self, request, *args, **kwargs):
        orden = Orden.objects.get(pk=request.POST['orden_id'])
        if not orden:
            return JsonResponse({'error': 'no existe la orden de trabajo'})
        try:
            orden.cancelar()
        except Exception as e:
            response = JsonResponse({'error': str(e)})
            response.status_code = 403  
            return response
        return JsonResponse({'data':'ok'})

class OrdenesList(ListView):
    model = Orden
    template_name = 'orden/ordenes.html'


class OrdenDelete(DeleteView):
    model = Orden
    template_name = 'orden/orden_delete.html'
    success_url = reverse_lazy('orden:orden_listar')

    @method_decorator(permission_required('orden.delete_orden', login_url='orden:orden_listar'))        
    def post(self, request, *args, **kwargs):
        return super(self.__class__, self).post(request,*args, **kwargs)


class OrdenDetail(DetailView):
    model = Orden
    template_name = 'orden/orden_ver.html'

    def get_context_data(self, **kwargs):
        contexto = super(self.__class__, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        orden = Orden.objects.get(pk=pk)
        contexto['tipos_tareas'] = orden.rubro.tipos_tareas_related
        contexto['tareas_presupuestadas'] = orden.tareas_presupuestadas
        return contexto

    @method_decorator(permission_required('orden.change_orden', login_url='orden:orden_listar'))        
    def post(self, request, *args, **kwargs):
        return super(self.__class__, self).post(request,*args, **kwargs)


class ClienteListado(ListView):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'data':render_to_string('orden/listado_clientes.html',{'clientes':Cliente.objects.all()})})


class EquipoListado(ListView):
    def get(self, request, *args, **kwargs):
        rubro = request.GET.get('rubro')

        return JsonResponse({'data':render_to_string('orden/listado_equipos.html',{'equipos':Equipo.objects.all()})})


class EquipoCreate(CreateView):
    model = Equipo
    template_name = 'equipo/equipo_form.html'
    form_class = EquipoForm
    success_url = reverse_lazy('orden:equipo_listar')

    @method_decorator(permission_required('orden.add_equipo', login_url='orden:orden_listar'))        
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class EquipoList(ListView):
    model = Equipo
    template_name = 'equipo/equipos.html'


class EquipoUpdate(UpdateView):
    model = Equipo
    template_name = 'equipo/equipo_form.html'
    form_class = EquipoForm
    success_url = reverse_lazy('orden:equipo_listar')

    @method_decorator(permission_required('orden.change_equipo', login_url='orden:orden_listar'))        
    def post(self, request, *args, **kwargs):
        return super(self.__class__, self).post(request,*args, **kwargs)


class EquipoDelete(DeleteView):
    model = Equipo
    template_name = 'equipo/equipo_delete.html'
    success_url = reverse_lazy('orden:equipo_listar')

    @method_decorator(permission_required('orden.delete_equipo', login_url='orden:orden_listar'))        
    def post(self, request, *args, **kwargs):
        return super(self.__class__, self).post(request,*args, **kwargs)


class EquipoCreatePopUp(EquipoCreate):
    template_name ='equipo/equipo_form_popup.html'
    success_url = '#'
