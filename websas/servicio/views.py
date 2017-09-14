from django.views.generic import TemplateView, CreateView
from django.core.urlresolvers import reverse_lazy
from .models import TipoServicio
from .forms import TipoServicioForm

# Create your views here.
class ServicioCreate(CreateView):
    model = TipoServicio
    template_name = 'servicio/servicio_detail.html'
    form_class = TipoServicioForm
    success_url = reverse_lazy('servicio:servicio_listar')

class ServicioList(TemplateView):
    template_name = 'servicio/servicios.html'