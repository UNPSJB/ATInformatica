from django import forms
from .models import Persona, Rol
from django.apps import apps
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


def get_roles_empleado():
    roles = Rol.TIPOS
    roles_empleados = []
    for r in roles:
        if r[0] != 0 and r[0] != 2 and r[0] != 10:
            roles_empleados.append(r)
    
    return roles_empleados

def get_rol_class(tipo_rol):
    rol = None
    for klass in Rol.__subclasses__():
        if klass.TIPO == tipo_rol:
            rol = klass
    return rol
        
class EmpleadoForm(PersonaForm):

    rol = forms.ChoiceField(choices=get_roles_empleado(), widget=forms.Select(attrs={'id':'input-tipo-rol', 'class':'form-control'}))

    def clean(self):
        if Persona.objects.filter(doc=self.cleaned_data['doc']).exists():
            persona = Persona.objects.get(doc=self.cleaned_data['doc'])
            # tipo_rol = int(self.cleaned_data['rol'])
            rol = get_rol_class(int(self.cleaned_data['rol']))

            if rol is None:
                raise forms.ValidationError("No existe el rol de empleado.")

            if persona.sos(rol):
                raise forms.ValidationError("El {} ya se encuentra registrado".format(rol.get_tipo_display()))

    def save(self):

        if not Persona.objects.filter(doc=self.cleaned_data['doc']).exists():
            persona = Persona(
                nombre=self.cleaned_data['nombre'],
                apellido=self.cleaned_data['apellido'],
                doc=self.cleaned_data['doc'],
                domicilio=self.cleaned_data['domicilio'],
                telefono=self.cleaned_data['telefono'],
                email=self.cleaned_data['email'])
            persona.save()
        else:
            persona = Persona.objects.get(doc=self.cleaned_data['doc'])

        tipo_rol = int(self.cleaned_data['rol'])
        rol = get_rol_class(int(self.cleaned_data['rol']))
        
        if rol is None:
            raise forms.ValidationError("No existe el rol")

        persona.agregar_rol(rol())

class EmpleadoAgragarRolForm(EmpleadoForm):

    persona_id = forms.IntegerField()


    def clean(self):
        
        if not Persona.objects.filter(pk=self.cleaned_data['persona_id']).exists():
            raise forms.ValidationError("No existe la persona")

        persona = Persona.objects.get(pk=self.cleaned_data['persona_id'])            
        rol = get_rol_class(int(self.cleaned_data['rol']))

        if rol is None:
            raise forms.ValidationError("No existe el rol")  

        if persona.sos(rol):
            raise forms.ValidationError("La persona ya tiene el rol")     

    def save(self, commit=True):
        
        persona = Persona.objects.get(pk=self.cleaned_data['persona_id'])
        rol = get_rol_class(int(self.cleaned_data['rol']))

        persona.agregar_rol(rol())
        return persona

    class Meta(EmpleadoForm.Meta):
        exclude = [
            'nombre',
            'apellido',
            'doc',
            'domicilio',
            'email',
            'telefono',
        ]
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