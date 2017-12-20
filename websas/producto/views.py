from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.core.urlresolvers import reverse_lazy
from .models import Producto
from .forms import ProductoForm, ProductoUpdateForm, ReservaCancelarForm, ReservaModificarForm
from reportes.forms import ReporteProductoForm
from sas.views import AjaxFormView
# Create your views here.

class ProductoCreate(CreateView):
    model = Producto
    template_name = 'producto/producto_form.html'
    form_class = ProductoForm
    success_url = reverse_lazy('producto:producto_listar')

    # @method_decorator(permission_required('producto.add_producto', login_url='producto:producto_listar'))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ProductoList(ListView):
    model = Producto
    template_name = 'producto/productos.html'

    
    def get_context_data(self, **kwargs):
        context = super(ProductoList, self).get_context_data(**kwargs)
        context["form"] = ReporteProductoForm()
        return context
    

class ProductoUpdate(UpdateView):
    model = Producto
    template_name = 'producto/producto_form.html'
    form_class = ProductoUpdateForm
    success_url = reverse_lazy('producto:producto_listar')

    def get(self, request, *args, **kwargs):
        res = super().get(request, *args, **kwargs)
        # import ipdb; ipdb.set_trace()
        return super().get(request, *args, **kwargs)


    @method_decorator(permission_required('producto.change_producto', login_url='producto:producto_listar'))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ProductoDelete(DeleteView):
    model = Producto
    template_name = 'producto/producto_delete.html'
    success_url = reverse_lazy('producto:producto_listar')

    @method_decorator(permission_required('producto.delete_producto', login_url='producto:producto_listar'))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class ProductoDetail(DetailView):
    model = Producto
    context_object_name = 'producto'
    template_name = 'producto/producto_detail.html'
    success_url = reverse_lazy('producto:producto_listar')

class ReservaCancelar(AjaxFormView):

    form_class = ReservaCancelarForm

class ReservaModificar(AjaxFormView):

    form_class = ReservaModificarForm
