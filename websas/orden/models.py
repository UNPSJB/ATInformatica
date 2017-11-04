from django.db import models
from persona.models import Cliente, Tecnico
from rubro.models import Rubro
from servicio.models import TipoServicio
from usuario.models import Usuario
from decimal import Decimal
from tarea.models import Tarea


class Orden(models.Model):
    """Modelo de Orden de Trabajo

    Nota: La Orden de Trabajo es la entidad principal del sistema
    """

    cliente = models.ForeignKey(Cliente, null=True,related_name="ordenes")
    rubro = models.ForeignKey(Rubro, related_name="ordenes")
    equipo = models.ForeignKey("Equipo", null=True, blank=True, related_name="ordenes")
    tipo_servicio = models.ForeignKey(TipoServicio, null=True, blank=True, related_name="ordenes")
    usuario = models.ForeignKey(Usuario, null=True, blank=True, related_name="ordenes")
    tecnico = models.ForeignKey(Tecnico, null=True, blank=True, related_name="ordenes")
    descripcion = models.CharField(max_length=500, null=True, blank=True)
    cerrada = models.BooleanField(default=False)
    cancelada = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.cliente, self.descripcion)

    @property
    def tareas_presupuestadas(self):
        tareas_presupuestadas = []
        for tarea in self.tareas.all():
            if tarea.estas_presupuestada():
                tareas_presupuestadas.append(tarea)
        return tareas_presupuestadas

    @property
    def tareas_pendientes(self):
        tareas_pendientes = []
        for tarea in self.tareas.all():
            if tarea.estas_pendiente():
                tareas_pendientes.append(tarea)
        return tareas_pendientes

    @property
    def tareas_realizadas(self):
        tareas_realizadas = []
        for tarea in self.tareas.all():
            if tarea.estas_realizada():
                tareas_realizadas.append(tarea)
        return tareas_realizadas

    @property
    def tareas_canceladas(self):
        tareas_canceladas = []
        for tarea in self.tareas.all():
            if tarea.estas_cancelada():
                tareas_canceladas.append(tarea)
        return tareas_canceladas

    @classmethod
    def crear(cls, usuario, cliente, tecnico, rubro, equipo,tipo_servicio, descripcion):
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
                 equipo=equipo,
                 tipo_servicio=tipo_servicio,
                 descripcion=descripcion)
        ot.save()
        return ot
    
    def agregar_tarea(self, tipo_tarea, observacion):
        """Agrega una tarea al estado de una OT"
        
        Args: 
            tarea (Tarea): la tarea a agregar a la Orden de Trabajo
        Raise:
            Exception si el rubro de la tarea es distinto al rubro de la Orden de Trabajo """
    
        if(self.rubro != tipo_tarea.rubro):
            raise Exception("***TAREAS EN ESTADO: no se pudo realizar la accion***")
        Tarea.crear(tipo_tarea=tipo_tarea, orden=self, observacion=observacion)

    def aceptar_tareas(self, tareas):
        if not self.cerrada and not self.cancelada:
            if type(tareas) != list:
                tareas = [tareas]
            
            [tarea.hacer("aceptar") for tarea in tareas]
    
    def finalizar_tareas(self, tareas):
        if not self.cerrada and not self.cancelada:
            if type(tareas) != list:
                tareas = [tareas]
        
        [tarea.hacer("finalizar") for tarea in tareas]
        

    def cancelar_tareas(self, tareas):
        if not self.cerrada and not self.cancelada:
            if type(tareas) != list:
                tareas = [tareas]
        
        [tarea.hacer("cancelar") for tarea in tareas]  

        if not self.tareas_pendientes and not self.tareas_presupuestadas and not self.tareas_realizadas:
            self.cancelar()

    def cancelar(self):
        self.cancelada = True
        self.save()

    def cerrar(self):
        self.cerrada = True
        self.save()

class Equipo(models.Model):
    nro_serie = models.IntegerField(unique=True)
    descripcion = models.CharField(max_length=250)
    rubro = models.ForeignKey(Rubro, null=True, blank=True, related_name = "equipos")

