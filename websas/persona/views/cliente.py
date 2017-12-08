from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from django.views.generic import View, CreateView, ListView, UpdateView, DeleteView, DetailView
from persona.models import Cliente, Persona
from persona.forms import PersonaForm, PersonaUpdateForm, EmpleadoForm

# class ClienteList(ListView):
#     model = Cliente
#     template_name = 'persona/clientes.html'
#     context_object_name = 'clientes'

#     def get_context_data(self, **kwargs):
#         context = super(ClienteList, self).get_context_data(**kwargs)
#         context['tabla_botones'] = True
#         return context

#     def get_queryset(self):
#         return Cliente.objects.all()


class ClienteList(ListView):
    model = Cliente
    template_name = 'persona/clientes.html'


class ClienteListJSON(ListView):
    model = Cliente

    def get(self, request):
        clientes = self.get_queryset()
        lista_clientes = []
        for cliente in clientes:
            cliente_datos = {
                'id': cliente.persona.id,
                'nombre': cliente.persona.get_nombre_completo(),
                'dni': cliente.persona.doc,
                'domicilio': cliente.persona.domicilio,
                'telefono': cliente.persona.telefono,
                'email': cliente.persona.email,
                'saldo': "-",
                'url_ver': reverse_lazy('cliente:cliente_ver', args=[cliente.persona.id]),
                'url_editar': reverse_lazy('cliente:cliente_editar', args=[cliente.persona.id]),
                'url_eliminar': reverse_lazy('cliente:cliente_eliminar', args=[cliente.persona.id]),
            }
            lista_clientes.append(cliente_datos)

        return JsonResponse({'data': lista_clientes})


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
            persona.agregar_rol(Cliente())
            persona.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


# TODO: debería devolver JSON con datos del nuevo cliente, cosa de pasarlo al parent
class ClienteCreatePopup(ClienteCreate):
    template_name = 'persona/cliente_form_popup.html'
    success_url = '#'

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse_lazy('cliente:cliente_crear_popup'))


class ClienteCreateAjax(ClienteCreate):

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        print(request.POST)

        if form.is_valid():
            persona = form.save()
            persona.agregar_rol(Cliente())
            persona.save()
            return JsonResponse(data={'data':'cliente creado'},status=200)
        else:
            return JsonResponse(data={'data':'fallo letal'}, status=403)

class ClienteUpdate(UpdateView):
    model = Persona
    template_name = 'persona/cliente_form.html'
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
