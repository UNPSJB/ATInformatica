# from django.views.generic import TemplateView
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

    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)

        # se esta haciendo el boludo el template
        context['tipos_servicios'] = "ahre"
        # context['tipos_servicios'] = TipoServicio.objects.all()
        return context
    # def post(self, request, *args, **kwargs):
        # self.object = self.get_object
        # form = self.form_class(request.POST)
        # if form.is_valid():        
        # return TipoServicio.objets.all()