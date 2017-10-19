from django.db import models
from persona.models import Cliente, Tecnico
from rubro.models import Rubro
from servicio.models import TipoServicio

# Create your models here.
class Orden(models.Model):

    cliente = models.ForeignKey(
        Cliente,
        null=True,
        related_name="ordenes"
    )

    rubro = models.ForeignKey(
        Rubro,
        related_name="ordenes"
    )

    equipo = models.ForeignKey(
        "Equipo",
        null=True,
        related_name="ordenes"
    )

    tipo_servicio = models.ForeignKey(
        TipoServicio,
        related_name="ordenes"
    )

    tecnico = models.ForeignKey(
        Tecnico,
        related_name="ordenes"
    )

class Equipo(models.Model):
    nro_serie = models.IntegerField(unique=True)
    descripcion = models.CharField(max_length=250)

