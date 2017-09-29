from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from persona.models import Gerente, Persona
from persona.forms import PersonaForm, EmpleadoForm
from persona.views.empleado import EmpleadoCreate, EmpleadoDelete, EmpleadoDetail, EmpleadoList, EmpleadoUpdate


class GerenteCreate(EmpleadoCreate):
    
    success_url = reverse_lazy('empleado:gerente:gerente_listar')
    template_name = 'persona/gerente_form.html'
         
    @method_decorator(permission_required('persona.add_gerente', login_url='empleado:gerente:gerente_listar'))        
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def crear_rol(self, persona):
        gerente = Gerente(persona=persona)
        gerente.save()

class GerenteList(EmpleadoList):

    template_name = 'persona/gerentes.html' 
    success_url = reverse_lazy('empleado:gerente:gerente_listar')
    
    def get_queryset(self):
        return Gerente.objects.all()

class GerenteUpdate(EmpleadoUpdate):

    template_name = 'persona/gerente_form.html' 
    success_url = reverse_lazy('empleado:gerente:gerente_listar')

    @method_decorator(permission_required('persona.change_gerente', login_url='empleado:gerente:gerente_listar'))        
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    
class GerenteDelete(EmpleadoDelete):

    template_name = 'persona/gerente_delete.html' 
    success_url = reverse_lazy('empleado:gerente:gerente_listar')

    @method_decorator(permission_required('persona.delete_gerente', login_url='empleado:gerente:gerente_listar'))        
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class GerenteDetail(EmpleadoDetail):

    template_name = 'persona/gerente_detail.html' 
    success_url = reverse_lazy('empleado:gerente:gerente_listar')
    
