from django.db import models
from django.contrib.auth.models import AbstractUser
from persona.models import Rol

from django.contrib.auth.models import UserManager

# Create your models here.

class Usuario(Rol, AbstractUser):
    primer_login = models.BooleanField(default=True)
    objects = UserManager()



