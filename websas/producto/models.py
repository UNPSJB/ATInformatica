from django.db import models
from django.db.models import Sum
from tarea.models import Tarea
from decimal import Decimal
from safedelete.models import SafeDeleteModel, SOFT_DELETE

class Producto(SafeDeleteModel):
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

    _safedelete_policy = SOFT_DELETE

    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50, null=True, blank=True)
    marca = models.CharField(max_length=20)
    stock_minimo = models.IntegerField()
    stock = models.IntegerField()
    precio = models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0'))

    def save(self, *args, **kwagrs):
        # Si es la primera vez que se va a guardar el producto
        is_new = self.pk is None

        if is_new:
            # este checkeo es solamente para la primera vez que se guarda, no siempre
            if self.__class__.objects.filter(nombre=self.nombre, marca=self.marca).exists():
                raise Exception("El producto ya se encuentra registrado")

        self.nombre = str.title(self.nombre)
        self.marca = str.title(self.marca)
        super(self.__class__, self).save(*args, **kwagrs)

    @property
    def stock_reservado(self):
        """ Propiedad de solo lectura que indica la cantidad de unidades reservadas
        para tareas a realizar.

        Returns:
            int """
        stock_reservado = self.reservas.all(
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


class ReservaStock(SafeDeleteModel):
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
    producto = models.ForeignKey(
        Producto, related_name="reservas"
    )
    tarea = models.ForeignKey(
        Tarea, on_delete=models.CASCADE, related_name="reservas"
    )
    precio_unitario = models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0'))
    cantidad = models.PositiveIntegerField()

    def save(self, *args, **kwagrs):

        # Verificar que sea la primera vez que se hace el save con el self.pk is None
        if self.__class__.objects.filter(producto=self.producto, tarea=self.tarea).exists():
            raise Exception("El producto {} ya se encuentra reservado para la tarea {}".format(self.producto, self.tarea))

        self.precio_unitario = self.producto.precio
        super(self.__class__, self).save(*args, **kwagrs)

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

    def usar_repuestos(self):
        """ Método para consumir los repuestos reservados """
        self.producto.stock -= self.cantidad
        self.producto.save()
        self.delete()
