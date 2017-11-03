from django.db import models
from rubro.models import Rubro
from usuario.models import Usuario
from decimal import Decimal

# Create your models here.
class TipoTarea(models.Model):
    """ Modelo para la gestión de tipos de tarea

    Attributes:
        nombre(str): nombre del tipo de tarea
        descripcion(str, opcional): descripción del tipo de tarea
        rubro(:obj: Rubro): rubro al que pertenece el tipo de tarea """

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
    """ Modelo para la gestión de las tareas de las Órdenes de Trabajo

    Attributes:
        tipo_tarea(:obj:TipoTarea): tipo de tarea de la tarea a gestionar
        orden(:obj:Orden): Órden de Trabajo para la cual se creó la tarea
        observacion(str, opcional): observación de la tarea
        productos(:[obj..]:Producto, opcional): colección de productos (repuestos) necesarios para la tarea
        precio(:obj: Decimal): precio de la tarea """

    tipo_tarea = models.ForeignKey(
        TipoTarea, related_name="tareas"
    )
    orden = models.ForeignKey(
        'orden.Orden', on_delete=models.CASCADE, related_name="tareas"
    )
    observacion = models.CharField(max_length=250, null=True, blank=True)
    productos = models.ManyToManyField('producto.Producto', through='producto.ReservaStock', related_name='tareas')
    precio = models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0'))
    objects = TareaManager()

    class Meta:
        unique_together = (("tipo_tarea", "orden"),)

    @property
    def nombre(self):
        """ Propiedad de sólo lectura que devuelve el nombre del tipo de tarea asociado a la tarea """
        return self.tipo_tarea.nombre
    
    @property
    def descripcion(self):
        """ Propiedad de sólo lectura que devuelve la descripción del tipo de tarea asociado a la tarea """
        return self.tipo_tarea.descripcion

    @property
    def rubro(self):
        """ Propiedad de sólo lectura que devuelve el rubro del tipo de tarea asociado a la tarea """
        return self.tipo_tarea.rubro

    def estas_presupuestada(self):
        """ Método que consulta si la tarea está en estado TareaPresupuestada 
        
        Returns:
            True si la el estado de la tarea es TareaPresupuestada, False si no """
        return isinstance(self.estado, TareaPresupuestada)

    def estas_pendiente(self):
        """ Método que consulta si la tarea está en estado TareaPendiente 
        
        Returns:
            True si la el estado de la tarea es TareaPendiente, False si no """
        return isinstance(self.estado, TareaPendiente)

    def estas_realizada(self):
        """ Método que consulta si la tarea está en estado TareaRealizada 
        
        Returns:
            True si la el estado de la tarea es TareaRealizada, False si no """
        return isinstance(self.estado, TareaRealizada)

    def estas_cancelada(self):
        """ Método que consulta si la tarea está en estado TareaCancelada 
        
        Returns:
            True si la el estado de la tarea es TareaCancelada, False si no """
        return isinstance(self.estado, TareaCancelada)

    @classmethod
    def crear(cls, tipo_tarea, orden, observacion):

        """ Método para la creación de nuevas tareas 
        
        Controla la existencia de una Tarifa para el TipoTarea y el TipoServicio,
        de lo contrario lanza excepción.
        Además setea el precio de la tarea en función del precio de la tarifa al 
        momento de la creación.

        Args:
            tipo_tarea(:obj:TipoTarea): tipo de tarea de la tarea a gestionar
            orden(:obj:Orden): Órden de Trabajo para la cual se creó la tarea
            observacion(str, opcional): observación de la tarea
        
        Returns:
            obj:Tarea 

        Raise:
            Exception (si no existe Tarifa para el tipo de tarea y el tipo de servicio) """

        tarea = cls(tipo_tarea=tipo_tarea, orden=orden, observacion=observacion)
        tarea.save()
        tipo_servicio = tarea.orden.tipo_servicio
        try:
            tarifa = tarea.tipo_tarea.tarifas.get(tipo_servicio=tipo_servicio)
        except Exception as e:
            tarea.delete()
            raise Exception("El tipo de tarea: {}, no se encuentra tarifada para el tipo de servicio {}".format(tipo_tarea, tipo_servicio))
        tarea.precio = tarifa.precio 
        tarea.save()
        tarea.hacer(accion=None)
        return tarea

    @property
    def estado(self):
        """ Método que retorna el estado actual de la tarea 
        
        Returns:
            TareaEstado """
        if self.estados.exists():
            return self.estados.latest().related()
    
    def estados_related(self):
        """ Método que retorna la lista de estados por los que pasó la tarea (incluyendo el actual) 
        
        Returns:
            [<TareaEstado>..] """
        return [estado.related() for estado in self.estados.all()]

    def hacer(self, accion, *args, **kwargs):
        """ Método que permite invocar a un método de un estado desde el objeto tarea

        Args:
            accion(str): nombre del método a invocar
            *args y **kwargs: los argumentos que se le pasarán al método

        Returns:
            TareaEstado, si el método es de transición crea la instancia correspondiente, 
            si no, devuelve el estado actual 

        Raise:
            Exception si se intenta invocar a un método que no existe en el estado actual  
        """
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
        [self.cancelar_reserva(reserva) for reserva in self.tarea.reservas.all()]
        return TareaCancelada(tarea=self.tarea)

    def reservar_stock(self, producto, cantidad):
        self.tarea.reservas.create(tarea=self, producto=producto, cantidad=cantidad)

    def cancelar_reserva(self, producto):
        reserva = self.tarea.reservas.get(producto=producto.id)
        if reserva:
            reserva.eliminar()
            return self
        raise Exception("***TAREA: no existe la reserva indicada***")

class TareaPresupuestada(EstadoTarea):
    """ Se espera que el cliente la acepte """
    TIPO = 1
    def aceptar(self):
        return TareaPendiente(tarea=self.tarea)

class TareaPendiente(EstadoTarea):
    """ Fue aceptada la tarea y ahora hay que realizarla """
    TIPO = 2
    def finalizar(self):
        if any(map(lambda reserva: not reserva.hay_stock, self.tarea.reservas.filter(activa=True))):
            raise Exception("No hay stock suficiente para completar la tarea")
        map(lambda reserva: reserva.usar_repuestos(), self.tarea.reservas.filter(activa=True))
        return TareaRealizada(tarea=self.tarea)

class TareaRealizada(EstadoTarea):
    TIPO = 3

    def cancelar(self):
        return self

    def cancelar_reserva(self):
        return self

    def reservar_stock(sell):
        return self

class TareaCancelada(EstadoTarea):
    TIPO = 4
    """ La tarea estaba aceptada y fue cancelada """

    def cancelar(self):
        return self

    def cancelar_reserva(self):
        return self

    def reservar_stock(sell):
        return self

for Klass in EstadoTarea.__subclasses__():
    EstadoTarea.register(Klass)