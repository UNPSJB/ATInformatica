from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Producto
from .forms import ProductoForm
# Create your views here.

class ProductoCreate(CreateView):
    model = Producto
    template_name = 'producto/producto_detail.html'
    form_class = ProductoForm
    success_url = reverse_lazy('producto:producto_listar')

class ProductoList(ListView):
    model = Producto
    template_name = 'producto/productos.html'

class ProductoUpdate(UpdateView):
    model = Producto
    template_name = 'producto/producto_detail.html'
    form_class = ProductoForm
    success_url = reverse_lazy('producto:producto_listar')

class ProductoDelete(DeleteView):
    model = Producto
    template_name = 'producto/producto_delete.html'
    success_url = reverse_lazy('producto:producto_listar')
