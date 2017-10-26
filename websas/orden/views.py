from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from .models import Orden, Equipo
from persona.models import Cliente, Tecnico, Persona
from rubro.models import Rubro

from .forms import OrdenForm
# Create your views here.

class OrdenCreate(CreateView):
    model = Orden
    template_name = 'orden/orden_detail.html'
    form_class = OrdenForm
    success_url = reverse_lazy('/')

    def get_context_data(self, **kwargs):
        # Llamar a super para recuperar el contexto original
        contexto = super(OrdenCreate, self).get_context_data(**kwargs)
        # Agregar lo que necesita la vista
        contexto['clientes'] = Cliente.objects.all()
        contexto['rubros'] = Rubro.objects.all()
        contexto['tecnicos'] = Tecnico.objects.all()
        return contexto
