from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

from persona.models import Tecnico, Persona
from persona.forms import PersonaForm, EmpleadoForm
from persona.views.empleado import EmpleadoCreate, EmpleadoDelete, EmpleadoDetail, EmpleadoList, EmpleadoUpdate


class TecnicoCreate(EmpleadoCreate):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.template_name = 'persona/tecnico_form.html' 
        self.success_url = reverse_lazy('tecnico:tecnico_listar')
    
    def post(self, request, *args, **kwargs):
        #if request.user.has_perm('persona.add_tecnico'):
        super().post(request, *args, **kwargs)
        import ipdb;ipdb.set_trace()
    
    def crear_rol(persona):
        tecnico = Tecnico(persona=persona)
        tecnico.save()

class TecnicoList(EmpleadoList):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.template_name = 'persona/tecnicos.html' 
        self.success_url = reverse_lazy('empleado:tecnico:tecnico_listar')

    def get_queryset(self):
        return Tecnico.objects.all()

class TecnicoUpdate(EmpleadoUpdate):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.template_name = 'persona/tecnico_form.html' 
        self.success_url = reverse_lazy('empleado:tecnico:tecnico_listar')

class TecnicoDelete(EmpleadoDelete):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.template_name = 'persona/tecnico_delete.html' 
        self.success_url = reverse_lazy('empleado:tecnico:tecnico_listar')

class TecnicoUpdate(EmpleadoDetail):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.template_name = 'persona/tecnico_detail.html' 
        self.success_url = reverse_lazy('empleado:tecnico:tecnico_listar')
