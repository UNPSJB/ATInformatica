from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import TipoServicio
from .forms import TipoServicioForm

# Create your views here.
class TipoServicioCreate(CreateView):
    model = TipoServicio
    template_name = 'servicio/servicio_detail.html'
    form_class = TipoServicioForm
    success_url = reverse_lazy('servicio:servicio_listar')

class TipoServicioList(ListView):
    model = TipoServicio
    template_name = 'servicio/servicios.html'

class TipoServicioUpdate(UpdateView):
    model = TipoServicio
    template_name = 'servicio/servicio_detail.html'
    form_class = TipoServicioForm
    success_url = reverse_lazy('servicio:servicio_listar')

class TipoServicioDelete(DeleteView):
    model = TipoServicio
    template_name = 'servicio/servicio_delete.html'
    success_url = reverse_lazy('servicio:servicio_listar')