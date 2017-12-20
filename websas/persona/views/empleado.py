from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse_lazy
from django.template import loader
from sas.views import AjaxFormView
from django.views.generic import CreateView, View, ListView, UpdateView, DeleteView, DetailView
from django.contrib.contenttypes.models import ContentType
from usuario.models import Usuario
from persona.models import Rol
from django.utils.decorators import method_decorator
from persona.models import  Persona, Cliente
from persona.forms import PersonaForm, EmpleadoAgragarRolForm, EmpleadoForm, EmpleadoUpdateForm

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

    def post(self, request, *args, **kwargs):
        persona = Persona.objects.get(pk=kwargs.get('pk'))
        for rol in persona.roles_related():
            persona.eliminar_rol(rol)
        super().post(request, *args, **kwargs)
        return HttpResponseRedirect(self.get_success_url())
        


class EmpleadoEliminarRol(View):
    

    def post(self, request, *args, **kwargs):

        if not Persona.objects.filter(pk=request.POST['persona_id']).exists():
            response = JsonResponse({'error':'No existe la persona'})
            response.status_code = 403
            return response

        if not Rol.objects.filter(pk=request.POST['rol_id']).exists():
            response = JsonResponse({'error':'No existe el rol'})
            response.status_code = 403
            return response


        persona = Persona.objects.get(pk=request.POST['persona_id'])
        rol = Rol.objects.get(pk=request.POST['rol_id'])
        persona.eliminar_rol(rol)

        url = reverse_lazy('empleado:empleado_ver', kwargs={'pk':persona.id})
        
        # Si la persona se elimina, debe volver al listado
        if persona.deleted is not None:
            url = reverse_lazy('empleado:empleado_listar')
        return JsonResponse({'data':'todo ok','url':url})

class EmpleadoAgregarRol(View):

    def post(self, request, *args, **kwargs):

        form = EmpleadoAgragarRolForm(request.POST or None)
        # import ipdb; ipdb.set_trace()

        if form.is_valid():

            persona = form.save()

            url = reverse_lazy('empleado:empleado_ver', kwargs={'pk':persona.id})
            return JsonResponse({'data':'todo ok','url':url})

        response = JsonResponse({'error':form.errors})
        response.status_code = 403
        return response

class EmpleadoList(ListView):
    model = Persona
    template_name = 'persona/empleados.html'

    def get_queryset(self): 
        query = Rol.objects.all().exclude(tipo=0).exclude(tipo=2).exclude(tipo=10).distinct('persona')
        return [r for r in query if Persona.objects.filter(id=r.persona.id)]
        

class EmpleadoDetail(DetailView):
    model = Persona
    context_object_name = 'empleado'
    template_name = 'persona/empleado_detail.html'
    success_url = reverse_lazy('empleado:empleado_listar')
    form_class = EmpleadoAgragarRolForm

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        self.persona = self.get_object()
        contexto['roles'] = self.persona.roles_related()
        form = self.form_class
        if form not in contexto:
            contexto['form'] = form 
        return contexto 
