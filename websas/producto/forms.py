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
            'descripcion':'Descripcion',
            'marca':'Marca',
            'stock_minimo':'Stock minimo',
            'stock':'Stock actual',
            'precio':'Precio',          
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'descripcion': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'marca': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'stock_minimo': forms.NumberInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'stock': forms.NumberInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'precio': forms.NumberInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
        }
