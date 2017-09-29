from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

from servicio.models import TipoServicio
from .models import Rubro, Tarea, Tarifa
from .forms import RubroForm
# Create your views here.
class RubroList(ListView):
    model = Rubro
    template_name = 'rubro/rubros.html'


class RubroCreate(CreateView):
    model = Rubro
    template_name = 'rubro/rubro_detail.html'
    form_class = RubroForm
    success_url = reverse_lazy('rubro:rubros')
    context_object_name = "contexto_form"

    @method_decorator(permission_required('rubro.add_rubro', login_url='rubro:rubros'))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def tipos_servicios(self):
        return TipoServicio.objects.all()