from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from persona.models import JefeTaller, Persona
from persona.forms import PersonaForm, EmpleadoForm
from persona.views.empleado import EmpleadoCreate, EmpleadoDelete, EmpleadoDetail, EmpleadoList, EmpleadoUpdate


class JefeTallerCreate(EmpleadoCreate):

    template_name = 'persona/jefe_form.html' 
    success_url = reverse_lazy('empleado:jefe:jefe_listar')
    
    @method_decorator(permission_required('persona.add_Gerente'))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def crear_rol(self, persona):
        jefe = JefeTaller(persona=persona)
        jefe.save()

class JefeTallerList(EmpleadoList):
    
    template_name = 'persona/jefes.html' 
    success_url = reverse_lazy('empleado:jefe:jefe_listar')
    
    def get_queryset(self):
        return JefeTaller.objects.all()

class JefeTallerUpdate(EmpleadoUpdate):
    
    template_name = 'persona/jefe_form.html' 
    success_url = reverse_lazy('empleado:jefe:jefe_listar')
    
class JefeTallerDelete(EmpleadoDelete):
    
    template_name = 'persona/jefe_form.html' 
    success_url = reverse_lazy('empleado:jefe:jefe_listar')
    
class JefeTallerDetail(EmpleadoDetail):
    
    template_name = 'persona/jefe_detail.html' 
    success_url = reverse_lazy('empleado:jefe:jefe_listar')
    