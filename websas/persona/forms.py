from django import forms
from .models import Persona, Rol

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
                'max_length' : ("Nombre demasiado largo. No debe exceder los 50 caracteres."),
            },
            'apellido': {
                'max_length' : ("Apellido demasiado largo. No debe exceder los 50 caracteres.")
            },
            # TODO: tipodoc - quizás debería ser un form Select()
            # 'tipodoc': {
            #     'max_length'  ("Codigo de documento invalido."),
            # }
            'doc': {
                'max_length' : ("Documento demasiado largo. No debe exceder los 20 caracteres."),
                'unique' : ('Ya existe persona con ese documento.'),
            },
            'telefono': {
                'max_length' : ("Teléfono demasiado largo. No debe exceder los 15 dígitos."),
            }
        }
        
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class':'form-control col-md-7 col-xs-12',
                'required':'required',
                'autofocus': True
                }), 
            'apellido': forms.TextInput(attrs={
                'class':'form-control col-md-7 col-xs-12',
                }),
            'doc': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12',
            'pattern':'numeric',
            'data-validate-minmax':'0,'
            }),
            'domicilio': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'email': forms.EmailInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'telefono': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12', 'type':'tel'}),
        }

class PersonaUpdateForm(PersonaForm):
    
    class Meta(PersonaForm.Meta):
        fields = [
            'nombre',
            'apellido',
            'doc',
            'domicilio',
            'email',
            'telefono',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class':'form-control col-md-7 col-xs-12',
                'required':'required',
                'readonly':'True',
                }), 
            'apellido': forms.TextInput(attrs={
                'class':'form-control col-md-7 col-xs-12',
                'required':'required',
                'readonly':'True',
                }),
            'doc': forms.TextInput(attrs={
                'class':'form-control col-md-7 col-xs-12', 
                'readonly':'True',
                }),
            'domicilio': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'email': forms.EmailInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'telefono': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12', 'type':'tel'}),
        }

class EmpleadoForm(PersonaForm):
    
    roles = forms.ModelChoiceField(queryset=Rol.objects.values("tipo").distinct().exclude(tipo=2).exclude(tipo=10).all())

class EmpleadoUpdateForm(PersonaUpdateForm):
    
    class Meta(PersonaUpdateForm.Meta):
        fields = [
            'nombre',
            'apellido',
            'doc',
            'domicilio',
            'email',
            'telefono',
        ]