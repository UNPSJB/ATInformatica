from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.http import JsonResponse
from django.views.generic import TemplateView
from rubro.models import Rubro
# Create your views here.
class TareaCreate(TemplateView):
    template_name = "tarea/tarea_detail.html"

    @method_decorator(permission_required('tarea.add_tarea', login_url='rubro:rubro_listar'))
    def post(self, request, id_rubro, *args, **kwargs):
        
        print("Rubro: {} \n ID: {}".format(Rubro.objects.get(id=id_rubro).nombre,id_rubro))
        # print(request.POST.get("tarea"))
        # print(request.POST.get("tipo_servicio"))
        # print(request.POST.get("precio"))
        
        data = {
            "coso": "coseno"
        }
        return redirect("tarea:tarea_crear", id_rubro)
        # return JsonResponse(data)

    def get(self, request, id_rubro, *args, **kwargs):
        print("TareaCreate RUBRO {}".format(id_rubro))
        return super().get(request, *args, **kwargs)