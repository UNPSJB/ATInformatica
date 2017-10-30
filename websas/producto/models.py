from django.db import models
from django.db.models import Sum
from tarea.models import Tarea
# Create your models here.
class Producto(models.Model):

    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)
    marca = models.CharField(max_length=20)
    stock_minimo = models.IntegerField()
    stock = models.IntegerField()
    precio = models.FloatField()

    @property
    def stockDisponible(self):
        return self.stock - self.reservas.filter(activa=True).values_list('producto').aggregate(Sum('cantidad')).get('cantidad__sum')

    @property
    def stockReservado(self): 
        return self.reservas.filter(activa=True).values_list('producto').aggregate(Sum('cantidad')).get('cantidad__sum')

    @property
    def stock_es_bajo(self):
        return self.stock_minimo >= self.stockDisponible

class ReservaStock(models.Model):
    activa = models.BooleanField(default=True)
    producto = models.ForeignKey(
        Producto, related_name="reservas"
    )
    tarea = models.ForeignKey(
        Tarea, related_name="reservas"
    )
    cantidad = models.PositiveIntegerField()

    class Meta:
        unique_together = (("producto", "tarea"),)

    def eliminar(self):
        self.activa = False
        self.save()
