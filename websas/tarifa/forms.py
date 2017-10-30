from django import forms
from .models import Tarifa

class TarifaForm(forms.ModelForm):

    class Meta:
        model = Tarifa
        fields = [
            'tipo_tarea',
            'tipo_servicio',
            'precio'
        ]
        labels = {
            'tipo_tarea':'Tipo de Tarea',
            'tipo_servicio':'Tipo de Servicio',
            'precio':'Precio'          
        }
        widgets = {
            'precio': forms.NumberInput(attrs={
                'class':'form-control col-md-7 col-xs-12'
                }),
        }