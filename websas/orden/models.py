from django.db import models
from persona.models import Cliente, Tecnico
from rubro.models import Rubro
from servicio.models import TipoServicio
from usuario.models import Usuario

class OrdenBaseManager(models.Manager):
    pass

class OrdenQuerySet(models.QuerySet):
    def en_estado(self, estados):
        if type(estados) != list:
            estados = [estados]
        return self.annotate(max_id=models.Max('estados__id')).filter(
            estados__id=models.F('max_id'),
            estados__tipo__in=[e.TIPO for e in estados])

OrdenManager = OrdenBaseManager.from_queryset(OrdenQuerySet)



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
        blank=True,
        related_name="ordenes"
    )

    tipo_servicio = models.ForeignKey(
        TipoServicio,
        related_name="ordenes"
    )

    usuario = models.ForeignKey(
        Usuario,
        related_name="ordenes"
    )

    tecnico = models.ForeignKey(
        Tecnico,
        related_name="ordenes"
    )


    descripcion = models.CharField(max_length=500)

    objects = OrdenManager()

    @property
    def estado(self):
        if self.estados.exists():
            return self.estados.latest().related()

    @classmethod
    def crear(cls, usuario, cliente, rubro, tipo_servicio, tareas=None):
        ot = cls(cliente=cliente,
                 usuario=usuario,
                 tecnico=usuario.persona.como(Tecnico),
                 rubro=rubro,
                 tipo_servicio=tipo_servicio)
        ot.save()
        ot.hacer(accion=None, usuario=usuario, observacion="Orden creada")
        return ot

    def estados_related(self):
        return [estado.related() for estado in self.estados.all()]

    def hacer(self, accion, usuario, *args, **kwargs):
        estado_actual = self.estado
        if estado_actual is not None and hasattr(estado_actual, accion):
            metodo = getattr(estado_actual, accion)
            estado_nuevo = metodo(self, *args, **kwargs)
            if estado_nuevo is not None:
                estado_nuevo.save()
        elif estado_actual is None:
            Creada(orden=self, usuario=usuario, *args, **kwargs).save()
        else:
            raise Exception("***ORDEN DE TRABAJO: no se pudo realizar la accion***")


class Estado(models.Model):
    TIPO = 0
    TIPOS = [
        (0, 'estado')
    ]
    orden = models.ForeignKey(Orden, related_name="estados")
    tipo = models.PositiveSmallIntegerField(choices=TIPOS)
    timestamp = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(Usuario, null=True, blank=True)

    class Meta:
        get_latest_by = 'timestamp'

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.tipo = self.__class__.TIPO
        super(Estado, self).save(*args, **kwargs)

    def related(self):

        #me devuelvo si soy una subclase de Estado,
        #si soy de la clase Estado, devuelvo la cadena "Human friendly" del choices de tipo
        #return self if self.__class__ != Estado else getattr(self, self.get_tipo_display())
        return self.__class__ != Estado and self or getattr(self, self.get_tipo_display())

    @classmethod
    def register(cls, klass):
        cls.TIPOS.append((klass.TIPO, klass.__name__.lower()))


class Creada(Estado):
    def diagnosticar(self):
        """El tecnico agrega las tareas a realizar en la OT"""
        pass

class Diagnosticada(Estado):
    def aceptar(self):
        """Cliente acepta todas las tareas propuestas por el tecnico"""
        pass
    def consensuar(self):
        """Cliente acepta parcialmente las tareas propuestas por el tecnico"""
        pass

    def cancelar(self):
        """El cliente no acepta ninguna tarea propuesta por el tecnico"""

class Aceptada(Estado):
    def diagnosticar(self):
        """El tecnico agrega nuevas tareas a la OT"""
        pass

    def cerrar(self):
        """Se terminaron todas las tareas presupuestadas exitosamente"""
        pass

    def cancelar(self):
        """El cliente decide cancelar el trabajo"""
        pass

    def descartar(self):
        """El tecnico decide cancelar el trabajo"""
        pass

class Cerrada(Estado):
    pass


class Equipo(models.Model):
    nro_serie = models.IntegerField(unique=True)
    descripcion = models.CharField(max_length=250)


for Klass in Estado.__subclasses__():
    Estado.register(Klass)
