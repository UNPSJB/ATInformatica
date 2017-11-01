from django.db import models
from servicio.models import TipoServicio

# Create your models here.

class Rubro(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField(max_length=100)

    def __str__(self):
        return '{}'.format(self.nombre)

    @property
    def tipos_tareas_related(self):
        return self.tipos_tareas.all()

    @property
    def equipos_related(self):
        return self.equipos.all()