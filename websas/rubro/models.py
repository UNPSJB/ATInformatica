from django.db import models
from django.apps import apps
from servicio.models import TipoServicio

# Create your models here.

class Rubro(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField(max_length=100)

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args, **kwargs)
        TipoTarea = apps.get_model("tarea", "TipoTarea")
        rdyp = TipoTarea(nombre="RDyP", descripcion="Revisión, Diagnóstico, y Presupuesto", rubro=self).save()

    @property
    def tipos_tareas_related(self):
        return self.tipos_tareas.all()

    @property
    def equipos_related(self):
        return self.equipos.all()
