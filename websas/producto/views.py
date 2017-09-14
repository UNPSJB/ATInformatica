from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.views.generic import CreateView, TemplateView
from django.core.urlresolvers import reverse_lazy
from .models import Producto
from .forms import ProductoForm
# Create your views here.

class ProductoCreate(CreateView):
    model = Producto
    template_name = 'producto/producto_detail.html'
    form_class = ProductoForm
    success_url = reverse_lazy('producto:producto_listar')

class ProductoList(TemplateView):
    template_name = 'producto/productos.html'
