from django.db import models
from django.contrib.auth.models import AbstractUser
from persona.models import Rol

from django.contrib.auth.models import UserManager
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

# Create your models here.

class Usuario(Rol,AbstractUser):

    def tiene_permiso(self, permiso):
        roles_de_usuario = Rol.objects.filter(persona=self.persona).all()
        print([r for r in roles_de_usuario])
        print([self.has_perm(permiso) for r in roles_de_usuario])
        return any([self.has_perm(permiso, r) for r in roles_de_usuario])

    objects = UserManager()

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Usuario

class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('persona',)}),
    )

