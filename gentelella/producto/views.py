from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.

def producto_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.
    print(">> REQUEST HTTP: " + str(request.method))
    if request.method == 'GET':
        print(request.GET)
    if request.method == 'POST':
        print(request.POST)

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    print(load_template)
    template = loader.get_template('producto/' + load_template)
    return HttpResponse(template.render(context, request))
