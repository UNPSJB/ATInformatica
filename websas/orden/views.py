from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect

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
from reportes.forms import ReporteTotalOrdenesForm

# Create your views here.
class OrdenCreate(CreateView):
    model = Orden
    template_name = 'orden/orden_nueva.html'
    form_class =OrdenForm
    # success_url = reverse_lazy('/')

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
        equipo = None
        if request.POST.get('equipo') != 'sin':
            equipo = Equipo.objects.get(pk=request.POST.get('equipo'))
        descripcion = request.POST.get('observacion')

        if persona.sos(Cliente):
            orden = Orden(usuario=request.user, cliente=persona.como(Cliente), tecnico=tecnico.como(Tecnico), rubro=rubro, tipo_servicio=servicio, descripcion=descripcion,equipo=equipo)
            orden.save()

            return JsonResponse({"data": reverse_lazy("orden:orden_ver", args=(orden.id, ))})

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
            orden.cancelar(usuario=request.user)
        except Exception as e:
            response = JsonResponse({'error': str(e)})
            response.status_code = 403
            return response
        return JsonResponse({'data':'ok'})

class OrdenesList(ListView):
    model = Orden
    template_name = 'orden/ordenes.html'


    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        context["form"] = ReporteTotalOrdenesForm()
        return context



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
        contexto['tipos_tareas'] = orden.rubro.tipos_tareas.all()
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
        return JsonResponse({'data':render_to_string('orden/listado_equipos.html',{'equipos':Equipo.objects.filter(rubro=rubro)})})


class EquipoCreate(CreateView):
    model = Equipo
    template_name = 'equipo/equipo_form.html'
    form_class = EquipoForm
    success_url = reverse_lazy('orden:equipo_listar')

class EquipoCreateJson(CreateView):

    model = Equipo
    form_class = EquipoForm

    @method_decorator(permission_required('orden.add_equipo', login_url='orden:orden_listar'))
    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            return JsonResponse(data={'data':'todo bien'},status=200)

        return JsonResponse(data={'data':'No se ha podido crear'},status=403)

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

class EquipoDetail(DetailView):
    model = Equipo
    template_name = 'equipo/equipo_detail.html'
    success_url = reverse_lazy('orden:equipo_listar')

    def get_context_data(self, *args,**kwargs):
        contexto = super().get_context_data(**kwargs)
        self.equipo = self.get_object()
        ordenes = self.equipo.ordenes.all()
        tareas = []
        for o in ordenes:
            tareas += o.tareas_realizadas

        contexto['tareas'] = tareas
        return contexto   

class EquipoCreatePopUp(EquipoCreate):
    template_name ='equipo/equipo_form_popup.html'
    success_url = '#'

    def dispatch(self, request, *args, **kwargs):
        self.rubro = Rubro.objects.get(id=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args,**kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(initial={'rubro':self.rubro})
        context['form'].fields['rubro'].widget.attrs['disabled'] = 'disabled'
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        form.is_valid()
        return HttpResponseRedirect('/orden/equipo/crear_popup/{}'.format(self.rubro.id),form.errors)




