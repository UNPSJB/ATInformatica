from django import forms
from .models import Orden
class OrdenForm(forms.ModelForm):

    class Meta:
        model = Orden
        fields = [
            'cliente',
            'rubro',
            'equipo',
            'tipo_servicio',
            'tecnico',
        ]  
        labels = {
            'cliente':'Cliente',
            'rubro':'Rubro',
            'equipo':'Numero de Serie del Equipo',
            'tipo_servicio':'Tipo de Servicio',
            'tecnico':'Tecnico',
        }
        widgets = {
        }
