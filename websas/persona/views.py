from django.shortcuts import render
from django.http import HttpResponse,request
from django.core.urlresolvers import reverse_lazy
from django.template import loader
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from usuario.models import Usuario

from .models import Tecnico, Cliente,Persona
from .forms import TecnicoForm, ClienteForm

# Create your views here.
class TecnicoList(ListView):
    model = Persona
    template_name = 'persona/tecnicos.html'

    def dispatch(self, request, *args, **kwargs):
        usuario = Usuario.objects.filter(username=request.user)
        print(usuario[0].tiene_permiso('persona.p1'))
        return super(TecnicoList,self).dispatch(request, *args, **kwargs)

class TecnicoCreate(CreateView):
    model = Persona
    template_name = 'persona/tecnico_detail.html'
    form_class = TecnicoForm
    success_url = reverse_lazy('tecnico:tecnico_listar')

class TecnicoUpdate(UpdateView):
    model = Persona
    template_name = 'persona/tecnico_detail.html'
    form_class = TecnicoForm
    success_url = reverse_lazy('tecnico:tecnico_listar')

class TecnicoDelete(DeleteView):
    model = Persona
    template_name = 'persona/tecnico_delete.html'
    success_url = reverse_lazy('tecnico:tecnico_listar')


class ClienteList(ListView):
    model = Persona
    template_name = 'persona/clientes.html'

class ClienteCreate(CreateView):
    model = Persona
    template_name = 'persona/cliente_detail.html'
    form_class = ClienteForm
    success_url = reverse_lazy('cliente:cliente_listar')

class ClienteUpdate(UpdateView):
    model = Persona
    template_name = 'persona/cliente_detail.html'
    form_class = ClienteForm
    success_url = reverse_lazy('cliente:cliente_listar')

class ClienteDelete(DeleteView):
    model = Persona
    template_name = 'persona/cliente_delete.html'
    success_url = reverse_lazy('cliente:cliente_listar')

"""
def tecnicos(request):
    context = {}
    template = loader.get_template('persona/tecnicos.html')
    return HttpResponse(template.render(context, request))

def tecnico(request):
    if request.method == 'GET':
        context = {}
        template = loader.get_template('persona/tecnico_detail.html')
        return HttpResponse(template.render(context, request))
"""


# Create your views here.
def clientes(request):
    context = {}
    template = loader.get_template('persona/clientes.html')
    return HttpResponse(template.render(context, request))

def cliente(request):
    if request.method == 'GET':
        context = {}
        template = loader.get_template('persona/cliente_detail.html')
        return HttpResponse(template.render(context, request))

def cliente_detail(request, pk):
    context = {}
    template = loader.get_template('persona/cliente_detail.html')
    return HttpResponse(template.render(context, request))
