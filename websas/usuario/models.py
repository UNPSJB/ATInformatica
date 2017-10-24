from django.db import models
from django.contrib.auth.models import AbstractUser
from persona.models import Rol

from django.contrib.auth.models import BaseUserManager

# Create your models here.
class CustomUserManager(BaseUserManager):

    def crear_usuario(self, username, password, persona):

        user = self.model(
            username = username,
            persona = persona,
            first_name = persona.nombre,
            last_name = persona.apellido,
            email = persona.email
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password):

        user = self.model(
            username = username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, persona):

        user = self.create_user(
            username = username,
            password = password,
            persona = persona,
            first_name = persona.nombre,
            last_name = persona.apellido,
            email = persona.email
        )
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):

        user = self.create_user(
            username = username,
            password = password
        )
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user

class Usuario(Rol, AbstractUser):
    TIPO = 10

    primer_login = models.BooleanField(default=True)

    objects = CustomUserManager()

Rol.register(Usuario)