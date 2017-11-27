from django.db import models
from django.apps import apps
from sas.models import ModeloBase
# Create your models here.
class TipoServicio(ModeloBase):
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField(max_length=100)

    def __str__(self):
        return "{}: {}".format(self.nombre, self.descripcion)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        
        super(self.__class__, self).save(*args, **kwargs)
        #para evitar problemas de referencias circulares, conseguimos los modelos 
        #con django.apss
        if is_new:
            TipoTarea = apps.get_model("tarea", "TipoTarea")
            Tarifa = apps.get_model("tarifa", "Tarifa")
            for tt in TipoTarea.objects.all():
                Tarifa(tipo_tarea=tt, tipo_servicio=self).save()
