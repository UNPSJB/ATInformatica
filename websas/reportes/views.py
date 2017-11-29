from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.




class Reportes(TemplateView):
    template_name = "reportes/reportes.html"