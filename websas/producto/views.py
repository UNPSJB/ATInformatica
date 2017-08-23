from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.


def producto(request):
    context = {}
    # Ver el tema de si es modificación o creación
    
    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1] + '.html'
    
    template = loader.get_template('producto/' + load_template)
    return HttpResponse(template.render(context, request))

def producto_detail(request):
    context = {}
    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1] 
    
    template = loader.get_template('producto/' + load_template)
    return HttpResponse(template.render(context, request))
