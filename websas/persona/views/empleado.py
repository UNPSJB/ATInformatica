from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.template import loader
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.contenttypes.models import ContentType
from usuario.models import Usuario
from persona.models import Rol
from django.utils.decorators import method_decorator
from persona.models import  Persona
from persona.forms import PersonaForm, EmpleadoForm

"""""""""""""""""""""""""""""""""""""""
Vistas de empleados
"""""""""""""""""""""""""""""""""""""""
class EmpleadoCreate(CreateView):
    model = Persona
    template_name = 'persona/tecnico_detail.html'
    form_class = EmpleadoForm
    success_url = reverse_lazy('empleado:tecnico:tecnico_listar')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            persona = form.save()
            self.crear_rol(persona)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))
    
    def crear_rol(self, persona):
        pass

class EmpleadoUpdate(UpdateView):
    model = Persona
    template_name = 'persona/tecnico_detail.html'
    form_class = PersonaForm
    success_url = reverse_lazy('empleado:tecnico:tecnico_listar')

class EmpleadoDelete(DeleteView):
    model = Persona
    template_name = 'persona/tecnico_delete.html'
    success_url = reverse_lazy('empleado:tecnico:tecnico_listar')

class EmpleadoList(ListView):
    model = Persona
    template_name = 'persona/tecnicos.html'

class EmpleadoDetail(DetailView):
    model = Persona
    template_name = 'persona/tecnico_ver.html'