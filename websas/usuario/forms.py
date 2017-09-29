from django.contrib.auth.forms import UserChangeForm, UserCreationForm
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