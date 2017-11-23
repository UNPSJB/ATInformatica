from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from persona.models import Tecnico, Persona
from persona.forms import PersonaForm, EmpleadoForm
from persona.views.empleado import EmpleadoCreate, EmpleadoDelete, EmpleadoDetail, EmpleadoList, EmpleadoUpdate


class TecnicoCreate(EmpleadoCreate):
    
    template_name = 'persona/tecnico_form.html'
    success_url = reverse_lazy('empleado:tecnico:tecnico_listar')
    _rol = Tecnico()

    @method_decorator(permission_required('persona.add_tecnico', login_url='empleado:tecnico:tecnico_listar'))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class TecnicoList(EmpleadoList):
    model = Tecnico
    template_name = 'persona/tecnicos.html' 
    success_url = reverse_lazy('empleado:tecnico:tecnico_listar')
    
    # def get_queryset(self):
    #     return Tecnico.objects.all()

class TecnicoUpdate(EmpleadoUpdate):

    template_name = 'persona/tecnico_form.html' 
    success_url = reverse_lazy('empleado:tecnico:tecnico_listar')

    @method_decorator(permission_required('persona.change_tecnico', login_url='empleado:tecnico:tecnico_listar'))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class TecnicoDelete(EmpleadoDelete):
    
    template_name = 'persona/tecnico_delete.html' 
    success_url = reverse_lazy('empleado:tecnico:tecnico_listar')
    
    @method_decorator(permission_required('persona.delete_tecnico', login_url='empleado:tecnico:tecnico_listar'))    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class TecnicoDetail(EmpleadoDetail):
    context_object_name = 'tecnico'
    template_name = 'persona/tecnico_detail.html' 
    success_url = reverse_lazy('empleado:tecnico:tecnico_listar')

