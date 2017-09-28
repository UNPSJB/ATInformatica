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
        error_messages = {
            'nombre': {
                'max_length' : ("This writer's name is too long."),
                'required' : ("Requeridisimo vieja"),
            },
            'doc': {
                'unique' : ('Ya existe persona con ese doc'),
            },
        }
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class':'form-control col-md-7 col-xs-12',
                'required':'required',
                }), 
            'apellido': forms.TextInput(attrs={
                'class':'form-control col-md-7 col-xs-12'
                }),
            'doc': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'domicilio': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'email': forms.EmailInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'telefono': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
        }


class EmpleadoForm(PersonaForm):
    
    class Meta(PersonaForm.Meta):
        fields = [
            'nombre',
            'apellido',
            'doc',
            'domicilio',
            'email',
            'telefono',
        ]


"""

"""