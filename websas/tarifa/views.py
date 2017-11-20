from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .models import Tarifa
from .forms import TarifaForm
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from tarea.models import TipoTarea
# Create your views here.

class TarifaUpdate(View):
    @method_decorator(permission_required('tarifa.add_tarifa', login_url='rubro:rubro_listar'))
    def post(self, request, *args, **kwargs):
        pk = int(request.POST.get("tarifa"))
        precio = request.POST.get("precio")

        tarifa = Tarifa.objects.get(pk=pk)
        tarifa.actualizar_precio(precio)

        data = {
            "precio": precio,
        }
        return JsonResponse(data)

# class TarifaCreate(CreateView):
#     model = Tarifa
#     template_name = 'tarifa/tarifa_form.html'
#     form_class =  TarifaForm
#     success_url = reverse_lazy('tarifa:tarifa_listar')

# class TarifaList(ListView):
#     model = Tarifa
#     template_name = 'tarifa/tarifas.html'

# class TarifaUpdate(UpdateView):
#     model = Tarifa
#     form_class = TarifaForm
#     template_name = 'tarifa/tarifa_form.html'
#     success_url = reverse_lazy('tarifa:tarifa_listar')
# class TarifaDelete(DeleteView):
#     model = Tarifa
#     template_name = 'tarifa/tarifa_delete.html'
#     success_url = reverse_lazy('tarifa:tarifa_listar')

# class TarifaDetail(DetailView):
#     model = Tarifa
#     context_object_name = 'tarifa'
#     template_name = 'tarifa/tarifa_detail.html'
#     success_url = reverse_lazy('tarifa:tarifa_listar')