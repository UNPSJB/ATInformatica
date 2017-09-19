from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator

from persona.models import Gerente, Persona
from persona.forms import PersonaForm, EmpleadoForm
from persona.views.empleado import EmpleadoCreate, EmpleadoDelete, EmpleadoDetail, EmpleadoList, EmpleadoUpdate


class GerenteCreate(EmpleadoCreate):
    
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.template_name = 'persona/gerente_form.html' 
        self.success_url = reverse_lazy('empleado:gerente:gerente_listar')
        
    def post(self, request, *args, **kwargs):
        if request.user.has_perm('persona.add_Gerente'):
            super().post(request, *args, **kwargs)

    def crear_rol(persona):
        gerente = Gerente(persona=persona)
        gerente.save()

class GerenteList(EmpleadoList):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.template_name = 'persona/gerentes.html' 
        self.success_url = reverse_lazy('empleado:gerente:gerente_listar')

    def get_queryset(self):
        return Gerente.objects.all()

class GerenteUpdate(EmpleadoUpdate):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.template_name = 'persona/gerente_form.html' 
        self.success_url = reverse_lazy('empleado:gerente:gerente_listar')

class GerenteDelete(EmpleadoDelete):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.template_name = 'persona/gerente_delete.html' 
        self.success_url = reverse_lazy('empleado:gerente:gerente_listar')

class GerenteDetail(EmpleadoDetail):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.template_name = 'persona/gerente_detail.html' 
        self.success_url = reverse_lazy('empleado:gerente:gerente_listar')

