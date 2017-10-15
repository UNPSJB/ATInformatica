from django.db import models
from tarea.models import Tarea
from servicio.models import TipoServicio
# Create your models here.
class Tarifa(models.Model):
    tarea = models.ForeignKey(
        Tarea, related_name="tarifas"
    )
    tipo_servicio = models.ForeignKey(
        TipoServicio, related_name="tarifas"
    )
    precio = models.FloatField()

    class Meta:
        unique_together = (("tarea", "tipo_servicio"),)