from django.db import models
from django.db.models import Sum
from tarea.models import Tarea
from decimal import Decimal

class Producto(models.Model):
    """ Modelo para la gestión de productos.

    El modelo establece la restriccion unique_together para nombre y marca. Ademas por ser estos
    atributos de tipo string se formatean las cadenas antes de ser persistida la instancia, redefiniendo
    el metodo save().

    Attributes:
        nombre (str): nombre del producto
        descripcion (str, opcional): descripción del producto
        marca (str): marca del producto 
        stock_minimo (int): cantidad mínima requerida en stock
        stock (int): cantidad de unidades en stock
        precio (:obj: `Decimal`): precio del producto """

    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50, null=True, blank=True)
    marca = models.CharField(max_length=20)
    stock_minimo = models.IntegerField()
    stock = models.IntegerField()
    precio = models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0'))

    class Meta:
        unique_together = (("nombre", "marca"),)

    def save(self, *args, **kwagrs):
        self.nombre = str.title(self.nombre)
        self.marca = str.title(self.marca)
        super(self.__class__, self).save(*args, **kwagrs)

    @property
    def stock_reservado(self): 
        """ Propiedad de solo lectura que indica la cantidad de unidades reservadas 
        para tareas a realizar. 
    
        Returns: 
            int """
        stock_reservado = self.reservas.filter(activa=True
                                ).values_list('producto'
                                ).aggregate(Sum('cantidad')
                                ).get('cantidad__sum')

        if stock_reservado:
            return stock_reservado
        return 0

    @property
    def stock_disponible(self):
        """ Propiedad de solo lectura que indica la cantidad de unidades disponibles 
        
        Returns:
            int """
        return self.stock - self.stock_reservado

    @property
    def stock_es_bajo(self):
        """ Propiedad de solo lectura que indica si el stock disponible está por debajo del 
        mínimo establecido.
        
        Returns:
            True si stock_minimo >= stock_disponible, False si no """
        return self.stock_minimo >= self.stock_disponible

class ReservaStock(models.Model):
    """ Modelo para la gestión de reservas de stock

    Las instancias del modelo Tarea pueden necesitar reservar stock. Esta clase tiene la 
    responsabilidad de gestionar ese aspecto del dominio. 

    Attributes:
        activa (bool, default True): indica si la reserva esta activa o fue cancelada (baja lógica)
        producto(:obj: Producto, ForeignKey): producto del cual se está reservando stock
        tarea(:obj: Tarea, ForeignKey): tarea para la cual se reserva el stock
        precio_unitario(:obj, Decimal): precio del producto al momento de crearse la reserva (valor histórico)
        cantidad(int): cantidad de unidades reservadas
    """
    activa = models.BooleanField(default=True)
    producto = models.ForeignKey(
        Producto, related_name="reservas"
    )
    tarea = models.ForeignKey(
        Tarea, on_delete=models.CASCADE, related_name="reservas"
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
        """ Propiedad de solo lectura que indica si el producto tiene stock para ser consumido
        por la reserva. 
        
        Returns:
            True si stock_disponible >= 0, False si no """
        return self.producto.stock_disponible >= 0

    @property
    def subtotal(self):
        """ Propiedad de solo lectura que devuelve el costo de la reserva 
        
        Returns:
            float
        """
        return self.precio_unitario * self.cantidad

    def eliminar(self):
        """ Método para dar de baja una reserva (baja lógica) """
        self.activa = False
        self.save()

    def usar_repuestos(self):
        """ Método para consumir los repuestos reservados """
        self.producto.stock -= self.cantidad
        self.producto.save()
        self.eliminar()
