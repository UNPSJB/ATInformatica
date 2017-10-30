from django import forms
from .models import TipoTarea

class TipoTareaForm(forms.ModelForm):

    class Meta:
        model = TipoTarea
        fields = [
            'nombre',
            'descripcion',
            'rubro'
        ]
        labels = {
            'nombre':'Nombre',
            'descripcion':'Descripcion',
            'rubro':'Rubro'          
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'descripcion': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
        }