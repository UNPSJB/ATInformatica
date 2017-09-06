from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.


def producto(request):
    context = {}
    # Ver el tema de si es modificación o creación
    
    # Pick out the html file name from the url. And load that template.
    template = loader.get_template('producto/productos.html')
    return HttpResponse(template.render(context, request))

def producto_detail(request):
    context = {}
    # Pick out the html file name from the url. And load that template.
    
    template = loader.get_template('producto/producto_detail.html')
    return HttpResponse(template.render(context, request))

def stock(request):
    context = {}

    template = loader.get_template('producto/stock.html')
    return HttpResponse(template.render(context,request))
