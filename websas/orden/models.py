from django.db import models
from persona.models import Cliente, Tecnico
from rubro.models import Rubro
from servicio.models import TipoServicio
from usuario.models import Usuario
from decimal import Decimal


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
    cerrada = models.BooleanField(default=False)
    cancelada = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.cliente, self.descripcion)



    @property
    def detalles(self):
        """Propiedad que devuelve los Detalles de Orden asociados a la Orden de Trabajo

        Nota: un Detalle de Orden, contiene la Tarea que se realizó y el valor (precio) de la 
        Tarifa de la Tarea en el momento en que se creó el Detalle
        """
        return self.estado.detalles

    @property
    def tareas_presupuestadas(self):
        tareas_presupuestadas = []
        for tarea in self.tareas.all():
            if tarea.presupuestada:
                tareas_presupuestadas.append(tarea)
        return tareas_presupuestadas



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
    
    def agregar_tarea(self, tarea):
        """Agrega una tarea al estado de una OT"
        
        Args: 
            tarea (Tarea): la tarea a agregar a la Orden de Trabajo
        Raise:
            Exception si el rubro de la tarea es distinto al rubro de la Orden de Trabajo 
        """
        if(self.rubro != tarea.tipo_tarea.rubro):
            raise Exception("***TAREAS EN ESTADO: no se pudo realizar la accion***")
        self.tareas.add(tarea)   

    


    

class Equipo(models.Model):
    nro_serie = models.IntegerField(unique=True)
    descripcion = models.CharField(max_length=250)
    rubro = models.ForeignKey(Rubro, null=True, blank=True, related_name = "equipos")

