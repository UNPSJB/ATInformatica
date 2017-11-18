from django.contrib.auth.forms import forms, UserChangeForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import password_validation
from django.contrib import messages
from .models import Usuario
from django.contrib.auth.models import Group

class RegistrarUsuarioForm(forms.ModelForm):

    persona_id = forms.IntegerField()

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



