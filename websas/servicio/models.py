from django.db import models

# Create your models here.
class TipoServicio(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField(max_length=100)

    def __str__(self):
        return "{} {}".format(self.nombre)