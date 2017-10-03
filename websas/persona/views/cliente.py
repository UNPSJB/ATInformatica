from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from persona.models import Cliente, Persona
from persona.forms import PersonaForm, PersonaUpdateForm, EmpleadoForm

class ClienteList(ListView):
    model = Cliente
    template_name = 'persona/clientes.html'

    def get_queryset(self):
        return Cliente.objects.all()

class ClienteCreate(CreateView):
    model = Persona
    template_name = 'persona/cliente_form.html'
    form_class = PersonaForm
    success_url = reverse_lazy('cliente:cliente_listar')

    @method_decorator(permission_required('persona.add_cliente', login_url='cliente:cliente_listar'))        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        if form.is_valid() and request.user.has_perm('persona.add_cliente'):
            persona = form.save()
            cliente = Cliente(persona=persona)
            cliente.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

class ClienteUpdate(UpdateView):
    model = Persona
    template_name = 'persona/cliente_detail.html'
    form_class = PersonaUpdateForm
    success_url = reverse_lazy('cliente:cliente_listar')

    @method_decorator(permission_required('persona.change_cliente', login_url='cliente:cliente_listar'))        
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ClienteDelete(DeleteView):
    model = Persona
    template_name = 'persona/cliente_delete.html'
    success_url = reverse_lazy('cliente:cliente_listar')

    @method_decorator(permission_required('persona.delete_cliente', login_url='cliente:cliente_listar'))        
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ClienteDetail(DetailView):
    model = Persona
    context_object_name = 'cliente'
    template_name = 'persona/cliente_detail.html'
    success_url = reverse_lazy('cliente:cliente_ver')
