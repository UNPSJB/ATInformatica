from django.db.utils import IntegrityError
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.template.loader import render_to_string
from django.views.generic import TemplateView, FormView, CreateView, ListView, UpdateView, DeleteView, DetailView
from django.views import View
from rubro.models import Rubro
from .models import TipoTarea, Tarea
from .forms import TipoTareaForm, ReservaForm, ObservacionForm, CrearTareaForm, AceptarTareaForm
from orden.models import Orden
from producto.models import Producto
from servicio.models import TipoServicio
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.core.urlresolvers import reverse_lazy

class ReservaCreate(View):

    @method_decorator(permission_required('producto.add_reserva', login_url='orden:orden_listar'))
    def post(self, request, *args, **kwargs):
        form = ReservaForm(request.POST or None)
        tarea = None
        producto = None
        
        if form.is_valid():
            tarea = Tarea.objects.get(pk=form.cleaned_data['tarea'])    
            producto = Producto.objects.get(pk=form.cleaned_data['producto'])
            cantidad = form.cleaned_data['cantidad']
        if tarea is None or producto is None:
            response = JsonResponse({'error': 'no es posible realizar la operación'})
            response.status_code = 403 
            return response
        tarea.hacer("reservar_stock", producto=producto, cantidad=cantidad)
        return JsonResponse({'data':'ok'})

class ObservacionCreate(View):

    @method_decorator(permission_required('tarea.add_observacion', login_url='orden:orden_listar'))
    def post(self, request, *args, **kwargs):
        form = ObservacionForm(request.POST or None)
        if form.is_valid():
            tarea = Tarea.objects.get(pk=form.cleaned_data['tarea'])
            contenido = form.cleaned_data['contenido']
        if tarea is None:
            response = JsonResponse({'error': 'no es posible realizar la operación'})
            response.status_code = 403 
            return response     
        tarea.hacer("agregar_observacion", usuario=request.user, contenido=contenido)
        return JsonResponse({'data':'ok'})

class TareaAceptar(View):

    @method_decorator(permission_required('tarea.change_tarea', login_url='orden:orden_listar'))
    def post(self, request, *args, **kwargs):
        # form = AceptarTareaForm(request.POST or None)
        # if form.is_valid():
        #     orden = Orden.objects.get(pk=form.cleaned_data['orden_id'])
        #     tareas = form.cleaned_data['tareas[]']
        orden = Orden.objects.get(pk=request.POST['orden_id'])
        tareas = request.POST.getlist('tareas[]')
        if orden is not None:
            try:
                orden.aceptar_tareas(tareas, usuario=request.user)
            except Exception as e:
                response = JsonResponse({'error': str(e)})
                response.status_code = 403  
                return response
            return JsonResponse({'data':'ok'})
        else:
            response = JsonResponse({'error': 'no es posible realizar la operación'})
            response.status_code = 403  
            return response         

class TareaFinalizar(View):
    @method_decorator(permission_required('tarea.change_tarea', login_url='orden:orden_listar'))
    def post(self, request, *args, **kwargs):
        orden = Orden.objects.get(pk=request.POST['orden_id'])
        tareas = request.POST.getlist('tareas[]')
        if orden is not None:
            try:
                orden.finalizar_tareas(tareas,usuario=request.user)
            except Exception as e:
                response = JsonResponse({'error': str(e)})
                response.status_code = 403  
                return response
            return JsonResponse({'data':'ok'})
        else:
            response = JsonResponse({'error': 'no es posible realizar la operación'})
            response.status_code = 403  
            return response  
class TareaCreate(View):    
    
    @method_decorator(permission_required('tarea.add_tarea', login_url='orden:orden_listar'))
    def post(self, request, *args, **kwargs):
        form = CrearTareaForm(request.POST or None)
        orden = None
        tipo_tarea = None
        if form.is_valid():
            tipo_tarea = TipoTarea.objects.get(pk=form.cleaned_data['tipo_tarea'])
            observacion = form.cleaned_data['observacion']
            orden = Orden.objects.get(pk=form.cleaned_data['orden_id'])
        if orden is None or tipo_tarea is None:
            response = JsonResponse({'error': 'No es posible realizar la operacion para esta tarea u orden.'})
            response.status_code = 403  
            return response 
        try:
            orden.agregar_tarea(tipo_tarea, observacion)
        except IntegrityError as err:
            print(err)
            response = JsonResponse({'error': 'La tarea no se puede agregar a la orden. Ya existe.'})
            response.status_code = 403
            return response
        except Exception as e:
            response = JsonResponse({'error': str(e)})
            response.status_code = 403  
            return response           
        return JsonResponse({'data':'ok'})

class TareaDetail(DetailView):
    model = Tarea
    context_object_name = 'tarea'
    template_name = 'tarea/tarea_ver.html'

    def get_context_data(self, **kwargs):
        contexto = super(self.__class__, self).get_context_data(**kwargs)
        contexto['productos'] = Producto.objects.all()
        return contexto


class TareaCambiarPrecio(View):
    @method_decorator(permission_required('tarea.change_tarea', login_url="orden:orden_listar"))
    def post(self, request, *args, **kwargs):
        pk = int(request.POST.get("tarea"))
        precio = request.POST.get("precio")

        tarea = Tarea.objects.get(pk=pk)
        tarea.actualizar_precio(precio)

        data = {
            "precio" : precio
        }

        return JsonResponse(data)
        
        
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
