from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse, Http404
from django.template.loader import render_to_string
from django.views.generic import TemplateView, FormView, CreateView, ListView, UpdateView, DeleteView, DetailView
from django.views import View
from rubro.models import Rubro
from .models import TipoTarea, Tarea
from .forms import TipoTareaForm
from orden.models import Orden
from producto.models import Producto
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
# Create your views here.
# class TareaCreate(TemplateView):
#     template_name = "tarea/tarea_detail.html"

#     @method_decorator(permission_required('tarea.add_tarea', login_url='rubro:rubro_listar'))
#     def post(self, request, id_rubro, *args, **kwargs):
        
#         print("Rubro: {} \n ID: {}".format(Rubro.objects.get(id=id_rubro).nombre,id_rubro))
#         # print(request.POST.get("tarea"))
#         # print(request.POST.get("tipo_servicio"))
#         # print(request.POST.get("precio"))
        
#         data = {
#             "coso": "coseno"
#         }
#         return redirect("tarea:tarea_crear", id_rubro)
#         # return JsonResponse(data)

#     def get(self, request, id_rubro, *args, **kwargs):
#         print("TareaCreate RUBRO {}".format(id_rubro))
#         return super().get(request, *args, **kwargs)

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
    # success_url = reverse_lazy('tarea:tipo_tarea_listar')

    def get(self, request, pk_rubro, *args, **kwargs):
        print("TareaCreate: RUBRO {}".format(pk_rubro))
        self.rubro = Rubro.objects.get(pk=pk_rubro)
        return super().get(request, *args, **kwargs)


    def post(self, request, pk_rubro, *args, **kwargs):
        nombre = request.POST["nombre"]
        descripcion = request.POST["descripcion"]
        
        tipo_tarea = TipoTarea(nombre=nombre, descripcion=descripcion, rubro=Rubro.objects.get(pk=pk_rubro))
        tipo_tarea.save()

        return redirect("rubro:tipo_tarea_crear", pk_rubro)

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        print("get_context_data: RUBRO {}".format(self.rubro.id))
        contexto["tareas"] = self.rubro.tipos_tareas.all()
        contexto["rubro"] = self.rubro
        return contexto
        

class TipoTareaList(ListView):
    model = TipoTarea
    template_name = 'tarea/tipos_tareas.html'

class TipoTareaUpdate(UpdateView):
    model = TipoTarea
    form_class = TipoTareaForm
    template_name = 'tarea/tipo_tarea_form.html'
    success_url = reverse_lazy('tarea:tipo_tarea_listar')

class TipoTareaDelete(DeleteView):
    model = TipoTarea
    template_name = 'tarea/tipo_tarea_delete.html'
    # success_url = reverse_lazy('rubro:tipo_tarea_crear')

    def get_success_url(self):
        return reverse_lazy("rubro:tipo_tarea_crear", args=(self.pk_rubro,))

    def get(self, request, *args, **kwargs):
        #Guardamos la pk del rubro
        self.pk_rubro = kwargs["pk_rubro"]
        self.pk = kwargs["pk"]
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto["rubro"] = Rubro.objects.get(pk=self.pk_rubro)
        contexto["tipo_tarea"] = TipoTarea.objects.get(pk=self.pk) 
        return contexto

    @method_decorator(permission_required('tarea.delete_tipo_tarea', login_url='rubro:rubro_listar'))
    def post(self, request, *args, **kwargs):
        pk_tarea = kwargs["pk"]
        tarea = TipoTarea.objects.get(pk=pk_tarea)
        
        #si la tarea es la RDyP, lo mandamos al patio
        if(tarea.nombre.lower() == "rdyp"):
            raise Http404("No se puede eliminar la RDyP")

        self.pk_rubro = kwargs["pk_rubro"]
        return super().post(request, *args, **kwargs)


class TipoTareaDetail(DetailView):
    model = TipoTarea
    context_object_name = 'tipo_tarea'
    template_name = 'tarea/tipo_tarea_detail.html'
    success_url = reverse_lazy('tarea:tipo_tarea_listar')
