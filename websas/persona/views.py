from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.
def tecnico(request):
    context = {}
    template = loader.get_template('persona/tecnicos.html')
    return HttpResponse(template.render(context, request))

def tecnico_detail(request, pk):
    context = {}
    template = loader.get_template('persona/tecnico_detail.html')
    return HttpResponse(template.render(context, request))

# Create your views here.
def cliente(request):
    context = {}
    template = loader.get_template('persona/clientes.html')
    return HttpResponse(template.render(context, request))

def cliente_detail(request, pk):
    context = {}
    template = loader.get_template('persona/cliente_detail.html')
    return HttpResponse(template.render(context, request))
