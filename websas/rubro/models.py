from django.db import models
from servicio.models import TipoServicio

# Create your models here.

class Rubro(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField(max_length=100)

class Tarea(models.Model):
    nombre = models.CharField(max_length=30)
    rubro = models.ForeignKey(
        Rubro, 
    )

class Tarifa(models.Model):
    tarea = models.ForeignKey(
        Tarea
    )
    tipo_servicio = models.ForeignKey(
        TipoServicio
    )
    precio = models.FloatField()

    class Meta:
        unique_together = (("tarea", "tipo_servicio"),)