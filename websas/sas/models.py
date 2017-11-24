from django.db import models

# Create your models here.

def BajasLogicasManagerFactory(activa):
    class ManagerBajasLogicas(models.Manager):
        def get_queryset(self):
            return super(ManagerBajasLogicas, self).get_queryset().filter(activa=activa)

    return ManagerBajasLogicas