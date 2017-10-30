from django.db import models
from rubro.models import Rubro
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

class TareaBaseManager(models.Manager):
    pass

class TareaQuerySet(models.QuerySet):
    def en_estado(self, estados):
        if type(estados) != list:
            estados = [estados]
        return self.annotate(max_id=models.Max('estados__id')).filter(
            estados__id=models.F('max_id'),
            estados__tipo__in=[e.TIPO for e in estados])

TareaManager = TareaBaseManager.from_queryset(TareaQuerySet)

class Tarea(models.Model):
    tipo_tarea = models.ForeignKey(
        TipoTarea
    )
    observacion = models.CharField(max_length=250)

    @classmethod
    def crear(cls, tipo_tarea, observacion):
        tarea = cls(tipo_tarea=tipo_tarea,
                 observacion=observacion)
        tarea.save()
        tarea.hacer(accion=None)
        return tarea

    @property
    def estado(self):
        if self.estados.exists():
            return self.estados.latest().related()
    
    def estados_related(self):
        return [estado.related() for estado in self.estados.all()]

    def hacer(self, accion, *args, **kwargs):
        estado_actual = self.estado
        if estado_actual is not None and hasattr(estado_actual, accion):
            metodo = getattr(estado_actual, accion)
            estado_nuevo = metodo(*args, **kwargs)
            if estado_nuevo is not None:
                estado_nuevo.save()
        elif estado_actual is None:
            TareaPresupuestada(tarea=self, *args, **kwargs).save()
        else:
            raise Exception("***ORDEN DE TRABAJO: no se pudo realizar la accion***")

    @property
    def nombre(self):
        return self.tipo_tarea.nombre
    
    @property
    def descripcion(self):
        return self.tipo_tarea.descripcion

    @property
    def rubro(self):
        return self.tipo_tarea.rubro


class EstadoTarea(models.Model):
    """Modelo de Estado para la Tarea"""
    TIPO = 0
    TIPOS = [
        (0, "estado")
    ]
    tarea = models.ForeignKey(Tarea, related_name="estados")
    tipo = models.PositiveSmallIntegerField(choices=TIPOS)
    timestamp = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(Usuario, null=True, blank=True)

    class Meta:
        get_latest_by = 'timestamp'

    @classmethod
    def register(cls, klass):
        cls.TIPOS.append((klass.TIPO, klass.__name__.lower()))

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.tipo = self.__class__.TIPO
        super(EstadoTarea, self).save(*args, **kwargs)

    def related(self):
        """Devuelve un objeto estado de la Tarea."""
        return self.__class__ != EstadoTarea and self or getattr(self, self.get_tipo_display())

    def cancelar(self):
        return TareaCancelada(tarea=self.tarea)

class TareaPresupuestada(EstadoTarea):
    """ Se espera que el cliente la acepte """
    TIPO = 1
    def aceptar(self):
        for reserva in self.tarea.reservas.filter(activa=True):
            if not reserva.hay_stock:
                return TareaEsperaRepuestos(tarea=self.tarea)
        return TareaPendiente(tarea=self.tarea)
    
class TareaEsperaRepuestos(EstadoTarea):
    """ No hay stock de repuestos para realizar el trabajo """
    TIPO = 2
    def desbloquear(self):
        hay_respuestos = True
        for reserva in self.tarea.reservas.filter(activa=True):
            if not reserva.hay_stock:
                hay_respuestos = False
        if not hay_respuestos:
            return self
        return TareaPendiente(tarea=self.tarea)


class TareaPendiente(EstadoTarea):
    """ Fue aceptada la tarea y ahora hay que realizarla """
    TIPO = 3
    def realizar(self):
        for reserva in self.tarea.reservas.filter(activa=True):
           reserva.usar_repuestos()
        return TareaRealizada(tarea=self.tarea)

class TareaRealizada(EstadoTarea):
    TIPO = 4

class TareaCancelada(EstadoTarea):
    TIPO = 5
    """ La tarea estaba aceptada y fue cancelada """

for Klass in EstadoTarea.__subclasses__():
    EstadoTarea.register(Klass)