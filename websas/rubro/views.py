from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from servicio.models import TipoServicio
from tarea.models import TipoTarea
from .models import Rubro
from .forms import RubroForm
# Create your views here.
class RubroList(ListView):
    model = Rubro
    template_name = 'rubro/rubros.html'


class RubroCreate(CreateView):
    model = Rubro
    template_name = 'rubro/rubro_detail.html'
    form_class = RubroForm
    # success_url = reverse_lazy('rubro:rubro_listar')

    @method_decorator(permission_required('rubro.add_rubro', login_url='rubro:rubro_listar'))
    def post(self, request, *args, **kwargs):
        res = super().post(request, *args, **kwargs)
        rdyp = TipoTarea(
            nombre="RDyP", descripcion="Revisión, Diagnóstico, y Presupuesto", rubro=self.object)
        rdyp.save()
        return res

    def get_success_url(self):
        return reverse_lazy('rubro:tipo_tarea_crear', args=(self.object.id, ))

    def tipos_servicios(self):
        return TipoServicio.objects.all()

class RubroUpdate(UpdateView):
    model = Rubro
    template_name = 'rubro/rubro_detail.html'
    form_class = RubroForm

    def get_success_url(self):
        print("RubroUpdate RUBRO {}".format(self.object.id))
        return reverse_lazy('rubro:tipo_tarea_crear', args=(self.object.id, ))

    @method_decorator(permission_required('rubro.change_rubro', login_url='rubro:rubro_listar'))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class RubroDelete(DeleteView):
    model = Rubro
    template_name = 'rubro/rubro_delete.html'
    success_url = reverse_lazy('rubro:rubro_listar')

    @method_decorator(permission_required('rubro.delete_rubro', login_url='rubro:rubro_listar'))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
