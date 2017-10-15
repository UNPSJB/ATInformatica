from django.db import models
from servicio.models import TipoServicio

# Create your models here.

class Rubro(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField(max_length=100)