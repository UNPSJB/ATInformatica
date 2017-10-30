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
# Create your views here.

# class TarifaCreate(View):
#     # username = request.GET.get('username', None)
#     # data = {
#     #     'is_taken': User.objects.filter(username__iexact=username).exists()
#     # }
#     # if data['is_taken']:
#     #     data['error_message'] = 'A user with this username already exists.'
#     @method_decorator(permission_required('tarifa.add_tarifa', login_url='rubro:rubro_listar'))
#     def post(self, request, *args, **kwargs):
#         print(request.POST.get("tarifa"))
#         print(request.POST.get("servicio"))
#         print(request.POST.get("precio"))
        
#         data = {
#             "coso": "coseno"
#         }
#         return JsonResponse(data)

class TarifaCreate(CreateView):
    model = Tarifa
    template_name = 'tarifa/tarifa_form.html'
    form_class =  TarifaForm
    success_url = reverse_lazy('tarifa:tarifa_listar')

class TarifaList(ListView):
    model = Tarifa
    template_name = 'tarifa/tarifas.html'

class TarifaUpdate(UpdateView):
    model = Tarifa
    form_class = TarifaForm
    template_name = 'tarifa/tarifa_form.html'
    success_url = reverse_lazy('tarifa:tarifa_listar')
class TarifaDelete(DeleteView):
    model = Tarifa
    template_name = 'tarifa/tarifa_delete.html'
    success_url = reverse_lazy('tarifa:tarifa_listar')

class TarifaDetail(DetailView):
    model = Tarifa
    context_object_name = 'tarifa'
    template_name = 'tarifa/tarifa_detail.html'
    success_url = reverse_lazy('tarifa:tarifa_listar')