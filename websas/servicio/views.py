from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView
from .models import TipoServicio
from .forms import TipoServicioForm

# Create your views here.
class TipoServicioCreate(CreateView):
    model = TipoServicio
    template_name = 'servicio/servicio_detail.html'
    form_class = TipoServicioForm
    success_url = reverse_lazy('servicio:servicio_listar')

    @method_decorator(permission_required('servicio.add_tiposervicio', login_url='servicio:servicio_listar'))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class TipoServicioList(ListView):
    model = TipoServicio
    template_name = 'servicio/servicios.html'

class TipoServicioUpdate(UpdateView):
    model = TipoServicio
    template_name = 'servicio/servicio_detail.html'
    form_class = TipoServicioForm
    success_url = reverse_lazy('servicio:servicio_listar')

    @method_decorator(permission_required('servicio.change_tiposervicio', login_url='servicio:servicio_listar'))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class TipoServicioDelete(DeleteView):
    model = TipoServicio
    template_name = 'servicio/servicio_delete.html'
    success_url = reverse_lazy('servicio:servicio_listar')

    @method_decorator(permission_required('servicio.delete_tiposervicio', login_url='servicio:servicio_listar'))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)