from django import forms
from .models import Orden, Equipo
from rubro.models import Rubro
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

class EquipoForm(forms.ModelForm):
    rubro = forms.ModelChoiceField(queryset=Rubro.objects.all())
    rubro.widget = forms.Select(attrs={
        'class': 'form-control col-md-7 col-xs-12',
    })

    class Meta:
        model = Equipo
        fields = [
            'nro_serie',
            'rubro',
            'descripcion'
        ]
        labels = {
            'nro_serie':'Número de Serie',
            'rubro':'Rubro',
            'descripcion':'Descripción'
        }
        error_messages = {
            'nro_serie': {
                'unique' : ("Ya existe un Equipo con el mismo Número de Serie"),
            },
        }
        widgets = {
            'nro_serie': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12', 'pattern': 'numeric', 'autofocus': True}),
            'descripcion': forms.TextInput(attrs={'class':'form-control'}),
        }

