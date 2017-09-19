from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator

from persona.models import JefeTaller, Persona
from persona.forms import PersonaForm, EmpleadoForm
from persona.views.empleado import EmpleadoCreate, EmpleadoDelete, EmpleadoDetail, EmpleadoList, EmpleadoUpdate


class JefeTallerCreate(EmpleadoCreate):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.template_name = 'persona/jefe_form.html' 
        self.success_url = reverse_lazy('empleado:jefe:jefe_listar')

    def post(self, request, *args, **kwargs):
        if request.user.has_perm('persona.add_tecnico'):
            super().post(request, *args, **kwargs)

    def crear_rol(persona):
        jefe = JefeTaller(persona=persona)
        jefe.save()

class JefeTallerList(EmpleadoList):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.template_name = 'persona/jefes.html' 
        self.success_url = reverse_lazy('empleado:jefe:jefe_listar')

    def get_queryset(self):
        return JefeTaller.objects.all()

class JefeTallerUpdate(EmpleadoUpdate):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.template_name = 'persona/jefe_form.html' 
        self.success_url = reverse_lazy('empleado:jefe:jefe_listar')

class JefeTallerDelete(EmpleadoDelete):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.template_name = 'persona/jefe_form.html' 
        self.success_url = reverse_lazy('empleado:jefe:jefe_listar')

class JefeTallerDetail(EmpleadoDetail):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.template_name = 'persona/jefe_detail.html' 
        self.success_url = reverse_lazy('empleado:jefe:jefe_listar')
