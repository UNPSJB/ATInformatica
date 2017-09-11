from django.db import models
from django.contrib.auth.models import AbstractUser
from persona.models import Rol

# Create your models here.

class Usuario(AbstractUser,Rol):

    def tiene_permiso(self, permiso):
        roles_de_usuario = Rol.objects.filter(persona=self.persona).all()
        print([r for r in roles_de_usuario])
        print([self.has_perm(permiso, r) for r in roles_de_usuario])
        return any([self.has_perm(permiso, r) for r in roles_de_usuario])

