from django import forms
from .models import Rubro

class RubroForm(forms.ModelForm):
    
    class Meta:
        model = Rubro
        fields = [
            'nombre',
            'descripcion'
        ]
        labels = {
            'nombre':'Nombre',
            'descripcion':'Descripcion'
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'descripcion': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
        }
