from django.contrib.auth.forms import forms, UserChangeForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import password_validation
from django.contrib import messages
from .models import Usuario

class RegistrarUsuarioForm(UserCreationForm):

    class Meta():
        model = Usuario
        fields = [
            'username',
            'password1',
            'password2', 
        ]

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        if commit:
            user.save()
        return user

class UsuarioUpdateForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = Usuario
        fields = [
            'username',
            'password',
        ]

class UsuarioCambiarPasswordForm(PasswordChangeForm):
    """
    Form que hereda de PasswordChangeForm para agregar clases al widget
    """

    old_password = forms.CharField(label=("Contraseña anterior"),
                                   widget=forms.PasswordInput(attrs={
                                       'class': 'form-control',
                                       'autofocus': 'True'
                                   }))
    
    new_password1 = forms.CharField(label=("Contraseña nueva"),
                                   widget=forms.PasswordInput(attrs={
                                       'class': 'form-control'
                                   }))

    new_password2 = forms.CharField(label=("Confirmar contraseña nueva"),
                                   widget=forms.PasswordInput(attrs={
                                       'class': 'form-control'
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