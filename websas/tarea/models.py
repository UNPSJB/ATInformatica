from django.db import models
from rubro.models import Rubro

# Create your models here.
class Tarea(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=100, null=True, blank=True)
    rubro = models.ForeignKey(
        Rubro, related_name="tareas"
    )

    def __str__(self):
        return "{}".format(self.nombre)