from django.db import models
from tarea.models import Tarea
from servicio.models import TipoServicio
from decimal import Decimal
# Create your models here.
class Tarifa(models.Model):
    tarea = models.ForeignKey(
        Tarea, related_name="tarifas"
    )
    tipo_servicio = models.ForeignKey(
        TipoServicio, related_name="tarifas"
    )
    precio = models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0'))

    class Meta:
        unique_together = (("tarea", "tipo_servicio"),)
