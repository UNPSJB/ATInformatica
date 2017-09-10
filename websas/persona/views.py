from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.template import loader
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from .models import Tecnico, Cliente
from .forms import TecnicoForm, ClienteForm

# Create your views here.
class TecnicoList(ListView):
    model = Tecnico
    template_name = 'persona/tecnicos.html'

class TecnicoCreate(CreateView):
    model = Tecnico
    template_name = 'persona/tecnico_detail.html'
    form_class = TecnicoForm
    success_url = reverse_lazy('tecnico:tecnico_listar')

class TecnicoUpdate(UpdateView):
    model = Tecnico
    template_name = 'persona/tecnico_detail.html'
    form_class = TecnicoForm
    success_url = reverse_lazy('tecnico:tecnico_listar')

class TecnicoDelete(DeleteView):
    model = Tecnico
    template_name = 'persona/tecnico_delete.html'
    success_url = reverse_lazy('tecnico:tecnico_listar')


class ClienteList(ListView):
    model = Cliente
    template_name = 'persona/clientes.html'

class ClienteCreate(CreateView):
    model = Cliente
    template_name = 'persona/cliente_detail.html'
    form_class = ClienteForm
    success_url = reverse_lazy('cliente:cliente_listar')

class ClienteUpdate(UpdateView):
    model = Cliente
    template_name = 'persona/cliente_detail.html'
    form_class = ClienteForm
    success_url = reverse_lazy('cliente:cliente_listar')

class ClienteDelete(DeleteView):
    model = Cliente
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
