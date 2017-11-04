from django.db import models
from persona.models import Cliente, Tecnico
from rubro.models import Rubro
from servicio.models import TipoServicio
from usuario.models import Usuario
from decimal import Decimal
from tarea.models import Tarea, TareaPendiente, TareaPresupuestada, TareaRealizada, TareaCancelada


class Orden(models.Model):
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

    def agregar_tarea(self, tipo_tarea, observacion):
        if(self.rubro != tipo_tarea.rubro):
            raise Exception("***TAREAS EN ESTADO: no se pudo realizar la accion***")
        Tarea.crear(tipo_tarea=tipo_tarea, orden=self, observacion=observacion)

    def _tareas_en_estado(self, estado):
        tareas_en_estado = []
        for tarea in self.tareas.all():
            if isinstance(tarea.estado, estado):
                tareas_en_estado.append(tarea)
        return tareas_en_estado

    @property
    def tareas_presupuestadas(self):
        return self._tareas_en_estado(TareaPresupuestada)

    @property
    def tareas_pendientes(self):
        return self._tareas_en_estado(TareaPendiente)

    @property
    def tareas_realizadas(self):
        return self._tareas_en_estado(TareaRealizada)

    @property
    def tareas_canceladas(self):
        return self._tareas_en_estado(TareaCancelada)

    def _hacer_en_tareas(self, ids_tareas, accion):
        if not self.cerrada and not self.cancelada:

            if type(ids_tareas) != list:
                ids_tareas = [ids_tareas]
            
            [tarea.hacer(accion) for tarea in self.tareas.filter(pk__in=ids_tareas)]

    def aceptar_tareas(self, ids_tareas):
        self._hacer_en_tareas(ids_tareas, "aceptar")
    
    def finalizar_tareas(self, ids_tareas):
        self._hacer_en_tareas(ids_tareas, "finalizar")

    def cancelar_tareas(self, ids_tareas):
        self._hacer_en_tareas(ids_tareas, "cancelar")

    def cancelar(self):
        if self.tareas_realizadas:
            raise Exception("La orden de trabajo nro: {} tiene tareas realizadas y no se puede cancelar".format(self.id))
        
        [tarea.hacer("cancelar") for tarea in self.tareas.all()]
        self.cancelada = True
        self.save()

    def cerrar(self):
        if self.tareas_pendientes:
            raise Exception("La orden de trabajo nro: {} tiene tareas pendientes y no se puede cerrar".format(self.id))
        self.cerrada = True
        self.save()

class Equipo(models.Model):
    nro_serie = models.IntegerField(unique=True)
    descripcion = models.CharField(max_length=250)
    rubro = models.ForeignKey(Rubro, null=True, blank=True, related_name = "equipos")
