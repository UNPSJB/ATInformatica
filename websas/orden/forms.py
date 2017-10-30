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
        },
        widgets = {
            'nro_serie': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'descripcion': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
        }

