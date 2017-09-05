from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

# Create your views here.

def index(request):
    context = {}
    template = loader.get_template('sas/index.html')
    return HttpResponse(template.render(context, request))