from django.db import models
from persona.models import Cliente, Tecnico
from rubro.models import Rubro
from servicio.models import TipoServicio
from usuario.models import Usuario
from decimal import Decimal
from tarea.models import Tarea, TareaPendiente, TareaPresupuestada, TareaRealizada, TareaCancelada

class Orden(models.Model):
    
    """ Orden de Trabajo. Entidad fundamental del sistema

    Attributes:
        cliente(:obj:Cliente): 
        rubro(:obj:Rubro):
        equipo(:obj:Equipo, opcional):
        tipo_servicio(:obj:TipoServicio):
        usuario(:obj:Usuario):
        tecnico(:obj:Tecnico):
        descripcion(str):
        cerrada(bool):
        cancelada(bool): """

    cliente = models.ForeignKey(Cliente, null=True,related_name="ordenes")
    rubro = models.ForeignKey(Rubro, related_name="ordenes")
    equipo = models.ForeignKey("Equipo", null=True, blank=True, related_name="ordenes")
    tipo_servicio = models.ForeignKey(TipoServicio, null=True, blank=True, related_name="ordenes")
    usuario = models.ForeignKey(Usuario, null=True, blank=True, related_name="ordenes")
    tecnico = models.ForeignKey(Tecnico, null=True, blank=True, related_name="ordenes")
    descripcion = models.CharField(max_length=500, null=True, blank=True)
    fecha = models.DateTimeField(auto_now=True)
    cerrada = models.BooleanField(default=False)
    cancelada = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.cliente, self.descripcion)

    @property
    def condicion(self):
        condicion = ""
        if self.cerrada:
            condicion = "cerrada"
        elif self.cancelada:
            condicion = "cancelada"
        else:
            condicion = "abierta"
        return condicion

    def agregar_tarea(self, tipo_tarea, observacion):
        
        """ Crea una tarea para la orden. 

        Args:
            tipo_tarea(:obj:TipoTarea): tipo de la tarea a crear 
            observacion(str): observacion
        
        Raise:
            Exeption si el rubro del tipo de tarea es distinto del rubro de la Orden """

        if(self.rubro != tipo_tarea.rubro):
            raise Exception("***TAREAS EN ESTADO: no se pudo realizar la accion***")
        Tarea.crear(tipo_tarea=tipo_tarea, orden=self, observacion=observacion)

    def _tareas_en_estado(self, estado):
        """Método privado que devuelve un subconjunto de tareas de la Oreden en un determinado estado
        
        Args: 
            estado(:cls: TareaEstado): denominación de una subclase de TareaEstado
        
        Returns:
            [<TareaEstado:obj>..] """

        tareas_en_estado = []
        for tarea in self.tareas.all():
            if isinstance(tarea.estado, estado):
                tareas_en_estado.append(tarea)
        return tareas_en_estado

    @property
    def tareas_presupuestadas(self):
        """Propiedad de solo lectura que un subconjunto de tareas de la Oreden en estado TareaPresupuestada 
        
        Returns:
            [<TareaPresupuestada:obj>..] """
        return self._tareas_en_estado(TareaPresupuestada)

    @property
    def tareas_pendientes(self):
        """Propiedad de solo lectura que un subconjunto de tareas de la Oreden en estado TareaPendiente 
        
        Returns:
            [<TareaPendiente:obj>..] """
        return self._tareas_en_estado(TareaPendiente)

    @property
    def tareas_realizadas(self):
        """Propiedad de solo lectura que un subconjunto de tareas de la Oreden en estado TareaRealizada 
        
        Returns:
            [<TareaRealizada:obj>..] """
        return self._tareas_en_estado(TareaRealizada)

    @property
    def tareas_canceladas(self):
        
        """Propiedad de solo lectura que un subconjunto de tareas de la Oreden en estado TareaCancelada 
        
        Returns:
            [<TareaCancelada:obj>..] """
        return self._tareas_en_estado(TareaCancelada)

    def _hacer_en_tareas(self, ids_tareas, accion):
        """ Método privado para realizar una acción en un conjunto de tareas
        
        Args:
            ids_tareas([int..]): ids del conjunto de tareas 
            accion(str): acción a relaizar """

        if not self.cerrada and not self.cancelada:

            if type(ids_tareas) != list:
                ids_tareas = [ids_tareas]
            
            [tarea.hacer(accion) for tarea in self.tareas.filter(pk__in=ids_tareas)]

    def aceptar_tareas(self, ids_tareas):
        """ Método que invoca _hacer_en_tareas ordenándole la accion "aceptar".

        Args:
            ids_tareas([int..]): ids del conjunto de tareas a aceptar """
        self._hacer_en_tareas(ids_tareas, "aceptar")
    
    def finalizar_tareas(self, ids_tareas):
        """ Método que invoca _hacer_en_tareas ordenándole la accion "finalizar".

        Args:
            ids_tareas([int..]): ids del conjunto de tareas a finalizar """
        self._hacer_en_tareas(ids_tareas, "finalizar")

    def cancelar_tareas(self, ids_tareas):
        """ Método que invoca _hacer_en_tareas ordenándole la accion "cancelar".

        Args:
            ids_tareas([int..]): ids del conjunto de tareas a cancelar """
        self._hacer_en_tareas(ids_tareas, "cancelar")

    def reservar_stock(self, id_tarea, producto, cantidad):
        tarea = self.tareas.get(pk=id_tarea)
        if not tarea:
            raise Exception ("No existe la tarea")
        tarea.reservar_stock(producto,  cantidad)

    def cancelar(self):
        """ Método para cancelar la orden de trabajo

        Raise: 
            Exception, si la orden de trabajo tiene tareas realizadas """
        if self.tareas_realizadas:
            raise Exception("La orden de trabajo nro: {} tiene tareas realizadas y no se puede cancelar".format(self.id))
        
        [tarea.hacer("cancelar") for tarea in self.tareas.all()]
        self.cancelada = True
        self.save()

    def cerrar(self):
        """ Método para cancelar la orden de trabajo

        Raise: 
            Exception, si la orden de trabajo tiene tareas pendientes """
        if self.tareas_pendientes:
            raise Exception("La orden de trabajo nro: {} tiene tareas pendientes y no se puede cerrar".format(self.id))
        self.cerrada = True
        self.save()

class Equipo(models.Model):
    nro_serie = models.IntegerField(unique=True)
    descripcion = models.CharField(max_length=250)
    rubro = models.ForeignKey(Rubro, null=True, blank=True, related_name = "equipos")

    def __str__(self):
        return "{}".format(self.descripcion)