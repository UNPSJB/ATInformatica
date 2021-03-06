from django.db import models
from persona.models import Cliente, Tecnico
from rubro.models import Rubro
from servicio.models import TipoServicio
from usuario.models import Usuario
from decimal import Decimal
from tarea.models import Tarea, TareaPendiente, TareaPresupuestada, TareaRealizada, TareaCancelada
from django.utils import timezone
from safedelete.models import SafeDeleteModel, SOFT_DELETE
import pytz

class Orden(SafeDeleteModel):
    """
    Orden de Trabajo. Entidad fundamental del sistema

    Atributos:
        - cliente(:obj: Cliente): Cliente titular de la Orden de trabajo.
        - rubro(:obj: Rubro): Rubro al que pertenecen la Orden de trabajo y sus tareas.
        - equipo(:obj: Equipo, opcional): Equipo asociado a la Orden de trabajo. Puede ser *null* si la Orden no lleva equipo.
        - tipo_servicio(:obj: TipoServicio): Tipo de servicio de la Orden de trabajo.
        - usuario(:obj: Usuario): Usuario que creó la Orden de trabajo.
        - tecnico(:obj: Tecnico): Técnico asignado a la Orden de trabajo.
        - descripcion(str): Descripción inicial del problema al momento de la creación. Puede estar en blanco.
        - cerrada(bool): Bandera - Verdadero si la Orden de trabajo está finalizada.
        - cancelada(bool): Bandera - Verdadero si la Orden de trabajo fue cancelada.
    """
    _safedelete_policy = SOFT_DELETE

    cliente = models.ForeignKey(Cliente, null=True,related_name="ordenes")
    rubro = models.ForeignKey(Rubro, related_name="ordenes")
    equipo = models.ForeignKey("Equipo", null=True, blank=True, related_name="ordenes")
    tipo_servicio = models.ForeignKey(TipoServicio, null=True, blank=True, related_name="ordenes")
    usuario = models.ForeignKey(Usuario, null=True, blank=True, related_name="ordenes")
    tecnico = models.ForeignKey(Tecnico, null=True, blank=True, related_name="ordenes")
    descripcion = models.TextField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    cerrada = models.BooleanField(default=False)
    cancelada = models.BooleanField(default=False)
    precio_final = models.DecimalField(
        decimal_places=2, max_digits=10, default=Decimal('0'))

    def __str__(self):
        return "{} {}".format(self.cliente, self.descripcion)

    @property
    def condicion(self):
        condicion = ""
        if self.cerrada:
            condicion = "Cerrada"
        elif self.cancelada:
            condicion = "Cancelada"
        else:
            condicion = "Abierta"
        return condicion

    def agregar_tarea(self, tipo_tarea, observacion):
        """
        Crea una tarea para la orden.

        Args:
            tipo_tarea(:obj: TipoTarea): Tipo de la tarea a crear.
            observacion(str): Observación del técnico sobre esta tarea al momento de la creación.

        Excepciones:
            Exception si el rubro del tipo de tarea es distinto del rubro de la Orden
        """

        if(self.rubro != tipo_tarea.rubro):
            raise Exception("***TAREAS EN ESTADO: no se pudo realizar la accion***")
        Tarea.crear(tipo_tarea=tipo_tarea, orden=self, observacion=observacion)

    def _tareas_en_estado(self, estado):
        """
        Método privado que devuelve un subconjunto de tareas de la Oreden en un determinado estado.

        Args:
            estado(:cls: TareaEstado): denominación de una subclase de TareaEstado.

        Returns:
            [<TareaEstado: obj>..]
        """

        tareas_en_estado = []
        for tarea in self.tareas.all():
            if isinstance(tarea.estado, estado):
                tareas_en_estado.append(tarea)
        return tareas_en_estado

    @property
    def tareas_presupuestadas(self):
        """
        Propiedad de solo lectura que un subconjunto de tareas de la Oreden en estado TareaPresupuestada

        Returns:
            [<TareaPresupuestada: obj>..]
        """
        return self._tareas_en_estado(TareaPresupuestada)

    @property
    def tareas_pendientes(self):
        """
        Propiedad de solo lectura que un subconjunto de tareas de la Oreden en estado TareaPendiente

        Returns:
            [<TareaPendiente: obj>..]
        """
        return self._tareas_en_estado(TareaPendiente)

    @property
    def tareas_realizadas(self):
        """
        Propiedad de solo lectura que un subconjunto de tareas de la Oreden en estado TareaRealizada

        Returns:
            [<TareaRealizada: obj>..] """
        return self._tareas_en_estado(TareaRealizada)

    @property
    def tareas_canceladas(self):

        """Propiedad de solo lectura que un subconjunto de tareas de la Oreden en estado TareaCancelada

        Returns:
            [<TareaCancelada: obj>..] """
        return self._tareas_en_estado(TareaCancelada)

    @property
    def tipos_tarea_agregables(self):
        """Devuelve los tipos de tarea que todavía no se hayan agregado a la Orden

        Returns:
            [<TipoTarea: obj>..]"""
        tipos_tareas = list(self.rubro.tipos_tareas.all())
        tipos_tareas_orden = list()

        for tarea in self.tareas.all():
            if not tarea.estas_cancelada():
                tipos_tareas_orden.append(tarea.tipo_tarea)

        return set(tipos_tareas) - set(tipos_tareas_orden)
    
    @property
    def precio_total(self):
        """ Devuelve el precio total de la orden """
        total = 0
        for tarea in self.tareas_realizadas:
            total += tarea.subtotal
        return total

    def _hacer_en_tareas(self, ids_tareas, accion,usuario):
        """ Método privado para realizar una acción en un conjunto de tareas

        Args:
            ids_tareas([int..]): ids del conjunto de tareas
            accion(str): acción a relaizar """

        if not self.cerrada and not self.cancelada:

            if type(ids_tareas) != list:
                ids_tareas = [ids_tareas]

            [tarea.hacer(accion,usuario=usuario) for tarea in self.tareas.filter(pk__in=ids_tareas)]

    def aceptar_tareas(self, ids_tareas,usuario):
        """ Método que invoca _hacer_en_tareas ordenándole la accion "aceptar".

        Args:
            ids_tareas([int..]): ids del conjunto de tareas a aceptar """
        self._hacer_en_tareas(ids_tareas, "aceptar",usuario=usuario)

    def finalizar_tareas(self, ids_tareas,usuario):
        """ Método que invoca _hacer_en_tareas ordenándole la accion "finalizar".

        Args:
            ids_tareas([int..]): ids del conjunto de tareas a finalizar """
        self._hacer_en_tareas(ids_tareas, "finalizar", usuario=usuario)

    def cancelar_tareas(self, ids_tareas,usuario):
        """ Método que invoca _hacer_en_tareas ordenándole la accion "cancelar".

        Args:
            ids_tareas([int..]): ids del conjunto de tareas a cancelar """
        self._hacer_en_tareas(ids_tareas, "cancelar",usuario=usuario)

    def reservar_stock(self, id_tarea, producto, cantidad):
        tarea = self.tareas.get(pk=id_tarea)
        if not tarea:
            raise Exception ("No existe la tarea")
        tarea.reservar_stock(producto,  cantidad)

    def cancelar(self, usuario):
        """ Método para cancelar la orden de trabajo """
        for tarea in self.tareas.all():
            if not tarea.estas_realizada:
                tarea.hacer("cancelar",usuario=usuario)
        self.cancelada = True
        self.fecha_fin = timezone.now()
        self.save()

    def cerrar(self):
        """ Método para cancelar la orden de trabajo

        Raise:
            Exception, si la orden de trabajo tiene tareas pendientes """
        if self.tareas_pendientes:
            raise Exception("La orden de trabajo nro: {} tiene tareas pendientes y no se puede cerrar".format(self.id))

        self.precio_final = self.precio_total
        self.cerrada = True
        self.fecha_fin = timezone.now()
        self.save()

    def tiene_repuestos(self):
        # si alguna tarea tiene una reserva, entonces, la orden tiene repuestos
        return any(map(lambda tarea: tarea.reservas_stock.count() > 0, self.tareas_realizadas))

    @property
    def total_repuestos(self):
        total_repuestos = 0
        for tarea in self.tareas_realizadas:
            total_repuestos += tarea.costo_repuestos
        return total_repuestos

    @property
    def total_mano_de_obra(self):
        total_mano_de_obra = 0
        for tarea in self.tareas_realizadas:
            total_mano_de_obra += tarea.precio
        return total_mano_de_obra

    @property
    def fecha(self):
        return self.fecha_fin.date()
class Equipo(SafeDeleteModel):
    """
    Modelo de Equipo para asociar a Ordenes de Trabajo y llevar registro de las mismas.

    Atributos:
        - nro_serie(int): Número de serie del equipo. Debe ser único.
        - descripcion(str): Descripción del equipo.
        - rubro(:obj: Rubro): Rubro bajo el que está categorizado el equipo.
    """
    nro_serie = models.IntegerField(unique=True)
    descripcion = models.CharField(max_length=250)
    rubro = models.ForeignKey(Rubro, null=True, blank=True, related_name = "equipos")

    def __str__(self):
        return "{}".format(self.descripcion)
