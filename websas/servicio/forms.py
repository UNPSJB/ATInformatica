from django import forms
from .models import TipoServicio

class TipoServicioForm(forms.ModelForm):

    class Meta:
        model = TipoServicio
        fields = [
            'nombre',
            'descripcion',
        ]
        labels = {
            'nombre':'Nombre',
            'descripcion':'Descripción',          
        }