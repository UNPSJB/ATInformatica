from django.db import models
from django.apps import apps
from servicio.models import TipoServicio
from sas.models import ModeloBase
from safedelete.models import SafeDeleteModel, SOFT_DELETE

# Create your models here.

class Rubro(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE

    nombre = models.CharField(max_length=30)
    descripcion = models.TextField(max_length=100)

    def __str__(self):
        return '{}'.format(self.nombre)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super(self.__class__, self).save(*args, **kwargs)

        if is_new:
            TipoTarea = apps.get_model("tarea", "TipoTarea")
            rdyp = TipoTarea(nombre="RDyP", descripcion="Revisión, Diagnóstico, y Presupuesto", rubro=self).save()

    @property
    def tipos_tareas_related(self):
        return self.tipos_tareas.all()

    @property
    def equipos_related(self):
        return self.equipos.all()
