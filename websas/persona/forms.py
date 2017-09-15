from django import forms
from .models import Persona

class PersonaForm (forms.ModelForm):

    class Meta:
        model = Persona
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


class EmpleadoForm(PersonaForm):
    ROLES = (
        ('TC', 'Tecnico'),
        ('JT', 'Jefe de Taller'),
        ('G', 'Gerente'),
    )
    rol = forms.ChoiceField(choices = ROLES, label="Tipo empleado", 
                              initial='', widget=forms.Select(), required=True)
    

    class Meta(PersonaForm.Meta):
        fields = [
            'nombre',
            'apellido',
            'doc',
            'domicilio',
            'email',
            'telefono',
            'rol',
        ]


"""
    def __init__(self, *args, **kwargs):
        super(EmpleadoForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['name', 'summary', 'description']
"""