from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from orden.models import Orden, Equipo
from persona.models import Cliente, Tecnico, Persona
from rubro.models import Rubro

from orden.forms import OrdenForm
# Create your views here.

class OrdenCreate(CreateView):
    model = Orden
    template_name = 'orden/orden_detail.html'
    form_class = OrdenForm

    success_url = reverse_lazy('/')

    def clientes(self):
        return Persona.objects.filter(pk__in=Cliente.objects.all().values('persona'))

    def rubros(self):
        return Rubro.objects.all()

    def tecnicos(self):
        return Persona.objects.filter(pk__in=Tecnico.objects.all().values('persona'))
