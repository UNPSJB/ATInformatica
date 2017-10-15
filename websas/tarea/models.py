from django.db import models
from rubro.models import Rubro

# Create your models here.
class Tarea(models.Model):
    nombre = models.CharField(max_length=30)
    rubro = models.ForeignKey(
        Rubro, related_name="tareas"
    )