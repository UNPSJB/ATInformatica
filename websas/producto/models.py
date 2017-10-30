from django.db import models
from django.db.models import Sum
from tarea.models import Tarea
from decimal import Decimal
# Create your models here.
class Producto(models.Model):

    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)
    marca = models.CharField(max_length=20)
    stock_minimo = models.IntegerField()
    stock = models.IntegerField()
    precio = models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0'))

    @property
    def stockReservado(self): 
        return self.reservas.filter(activa=True
            ).values_list('producto'
            ).aggregate(Sum('cantidad')
            ).get('cantidad__sum')

    @property
    def stockDisponible(self):
        return self.stock - self.stockReservado

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
    precio_unitario = models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0'))
    cantidad = models.PositiveIntegerField()

    class Meta:
        unique_together = (("producto", "tarea"),)

    def save(self, *args, **kwagrs):
        super(self.__class__, self).save(*args, **kwagrs)
        self.precio_unitario = self.producto.precio

    @property
    def hay_stock(self):
        return self.producto.stockDisponible >= 0

    def eliminar(self):
        self.activa = False
        self.save()

    def usar_repuestos(self):
        # print("Stock de la reserva {}, antes = {}".format(self.id, str(self.producto.stock)))
        self.producto.stock = self.producto.stock - self.cantidad
        self.producto.save()
        # print("Stock de la reserva {}, despues = {}".format(self.id, str(self.producto.stock)))
        # print("Estado antes {}".format(self.activa))
        self.activa = False
        self.save()
        # print("Estado despues {}".format(self.activa))