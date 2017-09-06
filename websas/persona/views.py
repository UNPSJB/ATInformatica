from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.
def persona(request):
    return render(request, 'persona/clientes.html', {})
