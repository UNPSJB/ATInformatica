from django import forms
from .models import Tecnico, Cliente

class TecnicoForm (forms.ModelForm):

    class Meta:
        model = Tecnico
        fields = [
            'nombre',
            'apellido',
            'doc',
            'domicilio',
            'email',
            'telefono',
        ]
        labels = {
            'nombre':'Nombre',
            'apellido':'Apellidos',
            'doc':'DNI',
            'domicilio':'Domicilio',
            'email':'Email',
            'telefono':'Telefono',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'apellido': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'doc': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'domicilio': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'email': forms.EmailInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'telefono': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
        }

class ClienteForm (forms.ModelForm):

    class Meta:
        model = Cliente
        fields = [
            'nombre',
            'apellido',
            'doc',
            'domicilio',
            'email',
            'telefono',
        ]
        labels = {
            'nombre':'Nombre',
            'apellido':'Apellidos',
            'doc':'DNI/CUIT/CUIL',
            'domicilio':'Domicilio',
            'email':'Email',
            'telefono':'Telefono',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'apellido': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'doc': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'domicilio': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'email': forms.EmailInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'telefono': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
        }