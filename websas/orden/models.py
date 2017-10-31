from django.db import models
from persona.models import Cliente, Tecnico
from rubro.models import Rubro
from servicio.models import TipoServicio
from usuario.models import Usuario
from decimal import Decimal

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

class Orden(models.Model):
    """Modelo de Orden de Trabajo

    Nota: La Orden de Trabajo es la entidad principal del sistema
    """

    # TODO: estoy poniendo todo null true para probar
    cliente = models.ForeignKey(Cliente, null=True,related_name="ordenes")
    rubro = models.ForeignKey(Rubro, related_name="ordenes")
    equipo = models.ForeignKey("Equipo", null=True, blank=True, related_name="ordenes")
    tipo_servicio = models.ForeignKey(TipoServicio, null=True, blank=True, related_name="ordenes")
    usuario = models.ForeignKey(Usuario, null=True, blank=True, related_name="ordenes")
    tecnico = models.ForeignKey(Tecnico, null=True, blank=True, related_name="ordenes")
    descripcion = models.CharField(max_length=500)

    objects = OrdenManager()

    def __str__(self):
        return "{} {}".format(self.cliente, self.descripcion)

    @property
    def estado(self):
        """Propiedad que devuelve el estado actual de la Orden de Trabajo"""
        if self.estados.exists():
            return self.estados.latest().related()

    @property
    def detalles(self):
        """Propiedad que devuelve los Detalles de Orden asociados a la Orden de Trabajo

        Nota: un Detalle de Orden, contiene la Tarea que se realizó y el valor (precio) de la 
        Tarifa de la Tarea en el momento en que se creó el Detalle
        """
        return self.estado.detalles

    @property
    def tareas(self):
        """Propiedad que devuelve las tareas agregadas a la Orden de Trabajo

        Nota: cuando una tarea se finaliza se remueve de la colección de Tareas y se crea
        un nuevo Detalle de Orden que la contiene
        """
        return self.estado.tareas

    @classmethod
    def crear(cls, usuario, cliente, tecnico, rubro, tipo_servicio, descripcion):
        """Método para crear una Orden de Trabajo

        Args:
            usuario (Usuario): es el usuario de la sección actual
            cliente (Cliente): es el cliente para el que se crea la Orden de Trabajo
            rubro   (Rubro): es el rubro para el cual se crea la Orden de Trabajo
            tipo_servicio (TipoServicio): es el tipo de servicio de la Orden de Trabajo
            descripcion (String): es una descripción de los problemas que el Cliente identificó
        
        Returns: 
            ot (Orden de Trabajo)
        """
        ot = cls(cliente=cliente,
                 usuario=usuario,
                 tecnico=tecnico,
                 rubro=rubro,
                 tipo_servicio=tipo_servicio,
                 descripcion=descripcion)
        ot.save()
        ot.hacer(accion=None, usuario=usuario)
        return ot

    def estados_related(self):
        """Método que devuelve los estados por los que pasó la Orden de Trabajo hasta el 
        estado actual inclusive
        """
        return [estado.related() for estado in self.estados.all()]

    def hacer(self, accion, *args, **kwargs):
        """Método fundamental para la implementación del patrón state. Reconoce métodos en Estados.

        Nota: recibe el nombre de un método y lo ejecuta si existe ese método en el estado actual. Mantiene consistente 
        el estado de la Orden de Trabajo si el método provoca una transición a otro estado.

        Args: 
            accion (string): es el nombre del método a ejecutar
            args y/o kwargs: los argumentos que recibirá el método
        """
        estado_actual = self.estado
        if estado_actual is not None and hasattr(estado_actual, accion):
            metodo = getattr(estado_actual, accion)
            estado_nuevo = metodo(*args, **kwargs)
            if estado_nuevo is not None:
                estado_nuevo.save()
        elif estado_actual is None:
            Creada(orden=self, *args, **kwargs).save()
        else:
            raise Exception("***ORDEN DE TRABAJO: no se pudo realizar la accion***")

    def agregar_detalle(self, tarea):
        """Agrega un Detalle de Orden a una OT

        Args: 
            tarea (Tarea): la tarea que se finalizó para la Orden de Trabajo
        Raise:
            Exception: si la tarea recibida es de un rubro distinto a la Orden de Trabajo
            Exception: si no existe tarifa para la tarea en el tipo de servicio
        """
        if(self.rubro != tarea.tipo_tarea.rubro):
            raise Exception("***AGREGAR DETALLE: tarea.rubro != orden.rubro***")
        tarifa = tarea.tipo_tarea.tarifas.get(tipo_servicio=self.tipo_servicio).precio
        if not tarifa:
            raise Exception("***AGREGAR DETALLE: no existe tarifa para el tipo de servicio y la tarea***")
        DetalleOrden(orden=self, tarea=tarea).save()


class DetalleOrden(models.Model):
    """Objeto 'item' o 'renglón' de la Orden de Trabajo

    Nota: contiene la tarea que se realizó y el precio de la misma
    """
    orden = models.ForeignKey(Orden, related_name="detalles")
    tarea = models.OneToOneField('tarea.Tarea')


class Estado(models.Model):
    """Modelo de Estado para la Orden de Trabajo"""
    TIPO = 0
    TIPOS = [
        (0, "estado")
    ]
    orden = models.ForeignKey(Orden, related_name="estados")
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
        super(Estado, self).save(*args, **kwargs)

    def related(self):
        """Devuelve un objeto estado de la Orden de Trabajo."""
        #me devuelvo si soy una subclase de Estado,
        #si soy de la clase Estado, devuelvo la cadena "Human friendly" del choices de tipo
        #return self if self.__class__ != Estado else getattr(self, self.get_tipo_display())
        return self.__class__ != Estado and self or getattr(self, self.get_tipo_display())

    def cancelar(self, motivo):
        """Transiciona la Orden de Trabajo al Estado Cancelada
        
        Args:
            motivo (String): observación de la razón de cancelación de la Orden de Trabajo
        """
        return Cancelada(orden=self.orden, motivo=motivo)

    def agregar_tarea(self, tipo_tarea, observacion):
        """Agrega una tarea al estado de una OT"
        
        Args: 
            tarea (Tarea): la tarea a agregar a la Orden de Trabajo
        Raise:
            Exception si el rubro de la tarea es distinto al rubro de la Orden de Trabajo 
        """
        if(self.orden.rubro != tipo_tarea.rubro):
            raise Exception("***TAREAS EN ESTADO: no se pudo realizar la accion***")
            
        self.tarea_set.create(tipo_tarea=tipo_tarea, observacion=observacion)
    
    def set_col_tareas(self, tareas):
        """Setea la colección de tareas a realizar para la Orden de Trabajo
        
        Args: 
            tareas ([Tarea..]): la colección de tareas a setear
        """
        for tarea in tareas:
            try:
                self.agregar_tarea(tarea)
            except:
                print("No se pudo agregar la tarea:")
                print(tarea)       
                
class Creada(Estado):
    """Estado inicial de la Orden de Trabajo 
    
    Nota: en este estado solo se puede diagnosticar o cancelar una Orden de Trabajo
    """
    TIPO = 1
    def diagnosticar(self, tareas):
        """El tecnico agrega las tareas a realizar en la OT
        
        Args: 
            tareas ([Tarea..]): la colección de tareas a agregar a la Orden de Trabajo
        Reuturns:
            diagnosticada (Diagnosticada): el estado nuevo al que transicionará la Orden de Trabajo
        """
        if not tareas:
            return self
        diagnosticada = Diagnosticada(orden=self.orden)
        diagnosticada.save()
        diagnosticada.set_col_tareas(tareas)
        return diagnosticada

class Diagnosticada(Estado):
    """ Estado Diagnosticada de la Orden de Trabajo 
    
    Nota: en este estado se puede aceptar, consensuar o cancelar una Orden de Trabajo
    """
    TIPO = 2

    # se agregan tareas en el estado Diagnosticada ? deberia hacerse con el método diagnosticar o con 
    # agregar_tarea ? 

    def aceptar(self):
        """Cliente acepta todas las tareas propuestas por el tecnico
        
        Returns:
            aceptada (Aceptada): el estado nuevo al que transicionará la Orden de Trabajo 
        """
        if not self.tareas.all():
            return self
        aceptada = Aceptada(orden=self.orden)
        aceptada.save()
        aceptada.set_col_tareas(self.tareas.all())
        return aceptada

    def consensuar(self, tareas):
        """Cliente acepta parcialmente las tareas propuestas por el tecnico
        
        Args: 
            tareas ([Tarea..]): las tareas que efectivamente fueron aceptadas por el cliente
        Returns:
            aceptada (Aceptada): el estado nuevo al que transicionará la Orden de Trabajo 
        """
        if not tareas:
            return self
        aceptada = Aceptada(orden=self.orden)
        aceptada.save()
        aceptada.set_col_tareas(tareas)
        return aceptada

class Aceptada(Estado):
    """Estado Aceptada de la Orden de Trabajo
    
    Nota: en este estado se puede cancelar, cerrar, diagnosticar, o finalizar_tarea en una Orden de Trabajo
    """
    TIPO = 3
    def diagnosticar(self, tareasnuevas):
        """El tecnico agrega nuevas tareas a la OT
        
        Args:
            tareasnuevas ([Tarea..]): coleccion de tareas a agregar a la Orden de Trabajo
        Returns:
            diagnosticada (Diagnosticada): estado al que transiciona la Orden de Trabajo 
        """

        if not tareasnuevas:
            return self
        tareas = [] 
        [tareas.append(tarea) for tarea in self.tareas.all()]
        [tareas.append(tarea) for tarea in tareasnuevas]
        diagnosticada = Diagnosticada(orden=self.orden)
        diagnosticada.save()
        diagnosticada.set_col_tareas(tareas)
        return diagnosticada

    def cerrar(self):
        """Se terminaron todas las tareas presupuestadas exitosamente
        
        Returns: 
            cerrada (Cerrada): el nuevo estado al que transiciona la Orden de Trabajo
        """
        if self.tareas.all().count() != 0:
            return self
        cerrada = Cerrada(orden=self.orden)
        cerrada.save()
        return cerrada

    def finalizar_tarea(self, tarea):
        """El tecnico finalizo una tarea exitosamente
        
        Args:
            tarea (Tarea): la tarea que se logró finalizar 
        """
        if not tarea:
            return self
        self.orden.agregar_detalle(tarea)
        self.tareas.remove(tarea)
        if self.tareas.all().count() == 0:
            return self.cerrar()

class Cerrada(Estado):
    TIPO = 4

class Cancelada(Estado): 
    TIPO = 5
    motivo = models.CharField(max_length=140)

class Equipo(models.Model):
    nro_serie = models.IntegerField(unique=True)
    descripcion = models.CharField(max_length=250)
    rubro = models.ForeignKey(
        Rubro,
        null=True,
        blank=True
        )


for Klass in Estado.__subclasses__():
    Estado.register(Klass)
