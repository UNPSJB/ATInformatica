from django.db import models

# Create your models here.

def BajasLogicasManagerFactory(activo):

    class ManagerBajasLogicas(models.Manager):
        
        use_for_related_fields = True
        
        def get_queryset(self):
            return super(ManagerBajasLogicas, self).get_queryset().filter(activo=activo)

    return ManagerBajasLogicas()
