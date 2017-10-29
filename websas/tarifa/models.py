from django.db import models
from tarea.models import TipoTarea
from servicio.models import TipoServicio
from decimal import Decimal
# Create your models here.
class Tarifa(models.Model):
    tipo_tarea = models.ForeignKey(
        TipoTarea, related_name="tarifas"
    )
    tipo_servicio = models.ForeignKey(
        TipoServicio, related_name="tarifas"
    )
    precio = models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0'))

    class Meta:
        unique_together = (("tipo_tarea", "tipo_servicio"),)
