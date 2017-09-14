from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = [
            'nombre',
            'descripcion',
            'marca',
            'stock_minimo',
            'stock',
            'precio',
        ]  
        labels = {
            'nombre':'Nombre',
            'descripcion':'Descripción',
            'marca':'Marca',
            'stock_minimo':'Satock mínimo',
            'stock':'Stock actual',
            'precio':'Precio',          
        }