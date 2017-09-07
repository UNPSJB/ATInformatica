from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='login')
def index(request):
    context = {}
    template = loader.get_template('sas/index.html')
    return HttpResponse(template.render(context, request))
