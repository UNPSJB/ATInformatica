from django.contrib.auth.forms import forms, UserChangeForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import password_validation
from django.contrib import messages
from .models import Usuario
from persona.models import Persona
from django.contrib.auth.models import Group

def registrarUsuarioFormFactory(persona_id):

    # TODO: reescribir _generate_username para asegurar unicidad (NO ATAJADA
    # EXCEPCION AL CREAR EL USUARIO, se debe asegurar en éste método)
    class RegistrarUsuarioForm(forms.Form):

        persona_id = forms.IntegerField()

        def _generate_username(self, persona):
            return str.lower(persona.nombre[0]) + str.lower(persona.apellido)

        def clean(self):
            cleaned_data = super(RegistrarUsuarioForm, self).clean()
            if not Persona.objects.filter(pk=cleaned_data.get('persona_id')).exists():
                raise forms.ValidationError(
                    "No existe la persona"
                )

        def save(self, commit=True):
            persona = Persona.objects.get(pk=self.cleaned_data['persona_id'])
            Usuario.objects.crear_usuario(username=self._generate_username(persona), 
                                        password=persona.doc, persona=persona)
            persona.agregar_rol(Usuario())

    return RegistrarUsuarioForm({'persona_id':persona_id})


class UsuarioCambiarPasswordForm(PasswordChangeForm):
    """
    Form que hereda de PasswordChangeForm para agregar clases al widget
    """

    old_password = forms.CharField(label=("Contraseña anterior"),
                                   widget=forms.PasswordInput(attrs={
                                       'class': 'form-control',
                                       'autofocus': True
                                   }))
    
    new_password1 = forms.CharField(label=("Contraseña nueva"),
                                   widget=forms.PasswordInput(attrs={
                                       'id': 'new_password1',
                                       'name': 'new_password1',
                                       'class': 'form-control'
                                   }))

    new_password2 = forms.CharField(label=("Confirmar contraseña nueva"),
                                   widget=forms.PasswordInput(attrs={
                                       'id': 'new_password2',
                                       'name': 'new_password2',
                                       'class': 'form-control',
                                       'data-validate-linked': '#new_password1'
                                   }))
    
    def save(self, commit=True):
        """
        Redefinición de save() para indicar el cambio de contraseña
        """
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.primer_login = False
            self.user.save()
        return self.user

class CrearGrupoForm(forms.ModelForm):
   
    class Meta:
        model = Group
        fields = ['name']
    
    def clean(self):
        cleaned_data = super(CrearGrupoForm, self).clean()
        nombre = cleaned_data.get('name')
        if Group.objects.filter(name=nombre).exists():
            raise forms.ValidationError(
                "El nombre del grupo no es válido"
            )



