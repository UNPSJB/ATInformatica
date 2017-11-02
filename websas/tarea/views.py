from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView, DetailView
from django.views import View
from rubro.models import Rubro
from .models import TipoTarea, Tarea
from .forms import TipoTareaForm
from orden.models import Orden
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

class TareaCreate(View):    
    
    # TODO: sanitizar las cadenas
    def post(self, request, *args, **kwargs):
        tipo_tarea = TipoTarea.objects.get(pk=request.POST['tipo_tarea'])
        observacion = request.POST['observacion']
        orden = Orden.objects.get(pk=request.POST['estado_orden'])
        orden.agregar_tarea(tipo_tarea, observacion)
        return JsonResponse({'data':'Todo mall'})

class TipoTareaCreate(CreateView):
    model = TipoTarea
    template_name = 'tarea/tipo_tarea_form.html'
    form_class =  TipoTareaForm
    success_url = reverse_lazy('tarea:tipo_tarea_listar')

class TipoTareaList(ListView):
    model = TipoTarea
    template_name = 'tarea/tipos_tareas.html'

class TipoTareaUpdate(UpdateView):
    model = TipoTarea
    form_class = TipoTareaForm
    template_name = 'tarea/tipo_tarea_form.html'
    success_url = reverse_lazy('tarea:tipo_tarea_listar')
class TipoTareaDelete(DeleteView):
    template_name = 'tarea/tipo_tarea_delete.html'
    success_url = reverse_lazy('tarea:tipo_tarea_listar')

class TipoTareaDetail(DetailView):
    model = TipoTarea
    context_object_name = 'tipo_tarea'
    template_name = 'tarea/tipo_tarea_detail.html'
    success_url = reverse_lazy('tarea:tipo_tarea_listar')