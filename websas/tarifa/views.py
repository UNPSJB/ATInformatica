from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .models import Tarifa
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from tarea.models import TipoTarea
from .forms import TarifaUpdateForm
from sas.views import AjaxFormView
# Create your views here.


        

class TarifaUpdate(AjaxFormView):
    
    form_class = TarifaUpdateForm
    
    @method_decorator(permission_required('tarifa.add_tarifa', login_url='rubro:rubro_listar'))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)