from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.template import loader
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.contenttypes.models import ContentType
from usuario.models import Usuario
from persona.models import Rol
from django.utils.decorators import method_decorator
from persona.models import  Persona, Cliente
from persona.forms import PersonaForm, EmpleadoForm, EmpleadoUpdateForm

"""""""""""""""""""""""""""""""""""""""
Vistas de empleados
"""""""""""""""""""""""""""""""""""""""
class EmpleadoCreate(CreateView):
    model = Persona
    form_class = PersonaForm
    template_name = 'persona/empleado_form.html'
    rol = " "

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            persona = form.save()
            # import ipdb; ipdb.set_trace()
            persona.agregar_rol(self.rol)
            persona.save()
            return HttpResponseRedirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(form=form))

class EmpleadoUpdate(UpdateView):
    model = Persona
    form_class = EmpleadoUpdateForm

class EmpleadoDelete(DeleteView):
    model = Persona

class EmpleadoList(ListView):
    model = Persona

class EmpleadoDetail(DetailView):
    model = Persona
