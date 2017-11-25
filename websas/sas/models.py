from django.db import models

# Create your models here.

def BajasLogicasManagerFactory(activo):

    class ManagerBajasLogicas(models.Manager):
        
        use_for_related_fields = True
        
        def get_queryset(self):
            return super(ManagerBajasLogicas, self).get_queryset().filter(activo=activo)

    return ManagerBajasLogicas()

class ModeloBase(models.Model):

    activo = models.BooleanField(default=True)

    objects = BajasLogicasManagerFactory(True)
    eliminados = BajasLogicasManagerFactory(False)
    todos = models.Manager()

    def delete(self):
        self.__class__.objects.filter(pk=self.id).update(activo = False)
    
    def eliminar(self):
        super().delete()

    class Meta:
        abstract = True

