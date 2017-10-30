from django.test import TestCase
from .models import Producto, ReservaStock

# Create your tests here.
class ProductoTest(TestCase):

    def setUp(self):
        self.producto = Producto(
            nombre="SSD", 
            descripcion="Disco de estado sólido",
            marca="Kingtong",
            stock_minimo=10,
            stock=20,
            precio=600
        )
        self.producto.save()

        # Reserva de 12 unidades del producto el stock mínimo del producto es 10
        self.reserva = ReservaStock(producto=self.producto, cantidad=12)
        self.reserva.save()
    
    def test_stock_disponible(self):
        self.assertEqual(self.producto.stockDisponible, 8)

    def test_stock_reservado(self):
        self.assertEqual(self.producto.stockReservado, 12)

    def test_stock_bajo(self):
        self.assertTrue(self.producto.stock_es_bajo)