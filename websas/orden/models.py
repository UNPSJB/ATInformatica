from django.db import models
from persona.models import Cliente, Tecnico
from rubro.models import Rubro
from servicio.models import TipoServicio

# Create your models here.
class Orden(models.Model):

    cliente = models.ForeignKey(
        Cliente,
        null=True
    )

    rubro = models.ForeignKey(
        Rubro
    )

    equipo = models.ForeignKey(
        "Equipo",
        null=True
    )

    tipo_servicio = models.ForeignKey(
        TipoServicio
    )

    tecnico = models.ForeignKey(
        Tecnico
    )

class Equipo(models.Model):
    nro_serie = models.IntegerField(unique=True)
    decripcion = models.CharField(max_length=250)

