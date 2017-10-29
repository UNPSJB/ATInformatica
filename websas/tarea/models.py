from django.db import models
from rubro.models import Rubro
from producto.models import Producto
from usuario.models import Usuario
from decimal import Decimal

# Create your models here.
class TipoTarea(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=100, null=True, blank=True)
    rubro = models.ForeignKey(
        Rubro, related_name="tipos_tareas"
    )

    def __str__(self):
        return "{}".format(self.nombre)


class Tarea(models.Model):
    tipo_tarea = models.ForeignKey(
        TipoTarea
    )
    repuesto = models.ForeignKey(
        Producto, null=True, blank=True
    )
    cantidad = models.PositiveIntegerField(default=1, null=True, blank=True)

    @property
    def nombre(self):
        return self.tipo_tarea.nombre
    
    @property
    def descripcion(self):
        return self.tipo_tarea.descripcion

    @property
    def rubro(self):
        return self.tipo_tarea.rubro













# class TareaBaseManager(models.Manager):
#     pass

# class TareaQuerySet(models.QuerySet):
#     def en_estado(self, estados):
#         if type(estados) != list:
#             estados = [estados]
#         return self.annotate(max_id=models.Max('estados__id')).filter(
#             estados__id=models.F('max_id'),
#             estados__tipo__in=[e.TIPO for e in estados])

# TareaManager = TareaBaseManager.from_queryset(TareaQuerySet)


# class EstadoTarea(models.Model):
#     """Modelo de Estado para la Tarea"""
#     TIPO = 0
#     TIPOS = [
#         (0, "estado")
#     ]
#     tarea = models.ForeignKey(Tarea, related_name="estados")
#     tarifa_tarea = models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0'))
#     tipo = models.PositiveSmallIntegerField(choices=TIPOS)
#     timestamp = models.DateTimeField(auto_now=True)
#     usuario = models.ForeignKey(Usuario, null=True, blank=True)

#     class Meta:
#         get_latest_by = 'timestamp'

#     @classmethod
#     def register(cls, klass):
#         cls.TIPOS.append((klass.TIPO, klass.__name__.lower()))

#     def save(self, *args, **kwargs):
#         if self.pk is None:
#             self.tipo = self.__class__.TIPO
#         super(EstadoTarea, self).save(*args, **kwargs)

#     def related(self):
#         """Devuelve un objeto estado de la Tarea."""
#         return self.__class__ != EstadoTarea and self or getattr(self, self.get_tipo_display())


# class TareaPresupuestada(EstadoTarea):
#     """ Se espera que el cliente la acepte """
#     TIPO = 1
    
# class TareaBloqueada(EstadoTarea):
#     """ No hay stock de repuestos para realizar el trabajo """
#     TIPO = 2

# class TareaPendiente(EstadoTarea):
#     """ Fue aceptada la tarea y ahora hay que realizarla """
#     TIPO = 3

# class TareaCancelada(EstadoTarea):
#     TIPO = 4
#     """ La tarea estaba aceptada y fue cancelada """