from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.template.loader import render_to_string
from django.views.generic import TemplateView, FormView, CreateView, ListView, UpdateView, DeleteView, DetailView
from django.views import View
from rubro.models import Rubro
from .models import TipoTarea, Tarea
from .forms import TipoTareaForm
from orden.models import Orden
from producto.models import Producto
from servicio.models import TipoServicio
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.core.urlresolvers import reverse_lazy

class ReservaCreate(View):
    # TODO: sanitizar las cadenas
    def post(self, request, *args, **kwargs):
        tarea = Tarea.objects.get(pk=request.POST['tarea'])
        producto = Producto.objects.get(pk=request.POST['producto'])
        cantidad = request.POST['cantidad']
        tarea.hacer("reservar_stock", producto=producto, cantidad=cantidad)
        return JsonResponse({'data':'Todo mall'})

class ObservacionCreate(View):

    def post(self, request, *args, **kwargs):
        # TODO: sanitizar las cadenas
        tarea = Tarea.objects.get(pk=request.POST['tarea'])
        contenido = request.POST['contenido']
        tarea.hacer("agregar_observacion", usuario=request.user, contenido=contenido)
        return JsonResponse({'data':'Todo mall'})

class TareaAceptar(View):

    def post(self, request, *args, **kwargs):
        orden = Orden.objects.get(pk=request.POST['orden_id'])
        tareas = request.POST.getlist('tareas[]')
        orden.aceptar_tareas(tareas)
        return JsonResponse({'data':'Todo mall'})

class TareaFinalizar(View):

    def post(self, request, *args, **kwargs):
        orden = Orden.objects.get(pk=request.POST['orden_id'])
        tareas = request.POST.getlist('tareas[]')
        orden.finalizar_tareas(tareas)
        return JsonResponse({'data':'Todo mall'})

class TareaCreate(View):    
    
    # TODO: sanitizar las cadenas
    def post(self, request, *args, **kwargs):
        tipo_tarea = TipoTarea.objects.get(pk=request.POST['tipo_tarea'])
        observacion = request.POST['observacion']
        orden = Orden.objects.get(pk=request.POST['estado_orden'])
        orden.agregar_tarea(tipo_tarea, observacion)
        return JsonResponse({'data':'Todo mall'})

class TareaDetail(DetailView):
    model = Tarea
    context_object_name = 'tarea'
    template_name = 'tarea/tarea_ver.html'

    def get_context_data(self, **kwargs):
        # Llamar a super para recuperar el contexto original
        contexto = super(self.__class__, self).get_context_data(**kwargs)
        contexto['productos'] = Producto.objects.all()
        return contexto

class TipoTareaCreate(FormView):
    # model = TipoTarea
    template_name = 'tarea/tipo_tarea_detail.html'
    form_class =  TipoTareaForm

    @method_decorator(permission_required('tarea.add_tipotarea', login_url='rubro:rubro_listar'))
    def dispatch(self, request, *args, **kwargs):
        #recuperamos el rubro
        #lo hacemos en el "dispatch" porque si no habia que hacerlo en el get,
        #y lo mismo en el post, porque serian dos objetos FormView distintos
        self.rubro = Rubro.objects.get(pk=kwargs["pk_rubro"])
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        nombre = request.POST["nombre"]
        descripcion = request.POST["descripcion"]
        
        tipo_tarea = TipoTarea(nombre=nombre, descripcion=descripcion, rubro=self.rubro)
        tipo_tarea.save()

        return redirect("rubro:tipo_tarea_crear", self.rubro.id)

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["tareas"] = self.rubro.tipos_tareas.all()
        contexto["rubro"] = self.rubro
        return contexto
        
class TipoTareaUpdate(UpdateView):
    model = TipoTarea
    form_class = TipoTareaForm
    template_name = 'tarea/tipo_tarea_edit.html'

    @method_decorator(permission_required('tarea.change_tipotarea', login_url='rubro:rubro_listar'))
    def dispatch(self, request, *args, **kwargs):
        self.rubro = Rubro.objects.get(pk=kwargs["pk_rubro"])
        self.tipo_tarea = TipoTarea.objects.get(pk=kwargs["pk"])

        #si la tarea es la RDyP, lo mandamos al patio
        if(self.tipo_tarea.nombre.lower() == "rdyp"):
            raise Http404("No se puede editar la RDyP")

        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("rubro:tipo_tarea_crear", args=(self.rubro.id,))

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class TipoTareaDelete(DeleteView):
    model = TipoTarea
    template_name = 'tarea/tipo_tarea_delete.html'

    @method_decorator(permission_required('tarea.delete_tipotarea', login_url='rubro:rubro_listar'))
    def dispatch(self, request, *args, **kwargs):
        self.rubro = Rubro.objects.get(pk=kwargs["pk_rubro"])
        self.tipo_tarea = TipoTarea.objects.get(pk=kwargs["pk"])

        #si la tarea es la RDyP, lo mandamos al patio
        if(self.tipo_tarea.nombre.lower() == "rdyp"):
            raise Http404("No se puede eliminar la RDyP")

        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy("rubro:tipo_tarea_crear", args=(self.rubro.id,))

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["rubro"] = self.rubro
        contexto["tipo_tarea"] = self.tipo_tarea 
        return contexto

    @method_decorator(permission_required('tarea.delete_tipo_tarea', login_url='rubro:rubro_listar'))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TipoTareaTarifar(TemplateView):
    template_name = 'tarea/tipo_tarea_tarifar.html'

    def dispatch(self, request, *args, **kwargs):
        self.tipo_tarea = TipoTarea.objects.get(pk=kwargs["pk"])
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["tipo_tarea"] = self.tipo_tarea
        return contexto


class TipoTareaDetail(DetailView):
    model = TipoTarea
    context_object_name = 'tipo_tarea'
    template_name = 'tarea/tipo_tarea_detail.html'
    success_url = reverse_lazy('tarea:tipo_tarea_listar')
