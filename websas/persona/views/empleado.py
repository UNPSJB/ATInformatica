from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse_lazy
from django.template import loader
from django.views.generic import CreateView, View, ListView, UpdateView, DeleteView, DetailView
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
    form_class = EmpleadoForm
    template_name = 'persona/empleado_form.html'
    success_url = reverse_lazy('empleado:empleado_listar')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(form=form))

class EmpleadoUpdate(UpdateView):
    model = Persona
    form_class = EmpleadoUpdateForm
    template_name = 'persona/empleado_form.html'
    success_url = reverse_lazy('empleado:empleado_listar')

class EmpleadoDelete(DeleteView):
    model = Persona
    template_name = 'persona/empleado_delete.html'
    success_url = reverse_lazy('empleado:empleado_listar')

    # def post(self, request, *args, **kwargs):
    #     # TODO: redefinir para eliminar el rol
    #     pass

class EmpleadoEliminarRol(View):
    
    def post(self, request, *args, **kwargs):
        # import ipdb; ipdb.set_trace()
        persona = Persona.objects.get(pk=request.POST['persona_id'])
        rol = Rol.objects.get(pk=request.POST['rol_id'])
        persona.eliminar_rol(rol)

        url = ''
        # Si la persona se elimina, debe volver al listado
        if persona.deleted is not None:
            url = reverse_lazy('empleado:empleado_listar')
        return JsonResponse({'data':'todo ok','url':url})

class EmpleadoList(ListView):
    model = Persona
    template_name = 'persona/empleados.html'

    def get_queryset(self): 
        return Rol.objects.all().exclude(tipo=0).exclude(tipo=2).exclude(tipo=10).distinct('persona')
        

class EmpleadoDetail(DetailView):
    model = Persona
    context_object_name = 'empleado'
    template_name = 'persona/empleado_detail.html'
    success_url = reverse_lazy('empleado:empleado_listar')

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        self.persona = self.get_object()
        contexto['roles'] = self.persona.roles_related()
        return contexto 