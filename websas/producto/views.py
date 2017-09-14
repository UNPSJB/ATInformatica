from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='usuario:login')
def producto(request):
    context = {}

    # SUGIERO QUE AQUÍ NOS FIJEMOS DE QUÉ MÉTODO ES
    # LA REQUEST Y DECIDIR SI MOSTRAR EL LISTADO O 
    # CREAR UNO NUEVO
    
    # Pick out the html file name from the url. And load that template.
    template = loader.get_template('producto/productos.html')
    return HttpResponse(template.render(context, request))

@login_required(login_url='usuario:login')
def producto_detail(request,id_producto):

    # Este señor de aquí nos devuelve un producto con clave 'id_producto'

    context = {}
    # Pick out the html file name from the url. And load that template.
    
    template = loader.get_template('producto/producto_detail.html')
    return HttpResponse(template.render(context, request))

def stock(request):
    context = {}

    template = loader.get_template('producto/stock.html')
    return HttpResponse(template.render(context,request))
