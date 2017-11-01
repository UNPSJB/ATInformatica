from django.test import TestCase
from .models import Producto, ReservaStock
from rubro.models import Rubro
from tarea.models import Tarea, TipoTarea
from tarifa.models import Tarifa
from servicio.models import TipoServicio
from usuario.models import Usuario
from orden.models import Orden
from persona.models import Cliente, Tecnico, Persona
# Create your tests here.
class ProductoTest(TestCase):

    def setUp(self):
        # Creamos una orden de trabajo para probar comportamiento de la reserva de stock 
        # frente a las tareas
        self.persona = Persona(
            nombre="Alguien",
            apellido="Alguien",
            doc="123321123",
            domicilio="cale213",
            email="l@l.com"
        )
        self.persona.save()
        self.persona.agregar_rol(Tecnico())
        self.persona.agregar_rol(Cliente())
        self.usuario = Usuario.objects.crear_usuario(username="Tecnico1", password="Tecnico1", persona=self.persona)
        self.persona.agregar_rol(Usuario())
        self.persona.save
        self.rubro = Rubro(nombre="Notebooks", descripcion="Reparación de notebooks")
        self.rubro.save()
        self.tipo_servicio = TipoServicio(nombre="Taller", descripcion="Reparación de equipos en taller")
        self.tipo_servicio.save()
        self.descripcion = "Ta destruida la máquina"

        self.orden = Orden.crear(self.usuario, 
            self.persona.como(Cliente), 
            self.persona.como(Tecnico), 
            self.rubro, 
            self.tipo_servicio, 
            self.descripcion
        )
        self.orden.save()

        # creamos un producto, tarifa y tarea para reservar stock
        self.producto = Producto(
            nombre="SSD", 
            descripcion="Disco de estado sólido",
            marca="Kingtong",
            stock_minimo=10,
            stock=20,
            precio=600
        )
        self.producto.save()
        self.tipo_tarea = TipoTarea(nombre="Cambio de disco", rubro=self.rubro)
        self.tipo_tarea.save()  
        self.tarifa = Tarifa(tipo_tarea=self.tipo_tarea, tipo_servicio=self.tipo_servicio, precio=300)
        self.tarifa.save()      
        self.tarea = Tarea.crear(
            tipo_tarea=self.tipo_tarea,
            orden=self.orden,
            observacion="Guardar el disco viejo")
        self.tarea.save()

        # Reserva de 12 unidades del producto el stock mínimo del producto es 10
        self.reserva = ReservaStock(tarea=self.tarea, producto=self.producto, cantidad=12)
        self.reserva.save()
    
    def test_stock_disponible(self):
        self.assertEqual(self.producto.stockDisponible, 8)

    def test_stock_reservado(self):
        self.assertEqual(self.producto.stockReservado, 12)

    def test_stock_bajo(self):
        self.assertTrue(self.producto.stock_es_bajo)

    def test_precio(self):
        # testeamos que al cambiar el precio del producto no cambie en la reserva
        self.producto.precio=400
        self.producto.save()
        self.assertFalse(self.producto.precio == self.reserva.precio_unitario)
        self.assertEqual(self.reserva.precio_unitario, 600)

    def test_subtotal(self):
        subtotal = self.reserva.precio_unitario * self.reserva.cantidad
        self.assertTrue(subtotal == self.reserva.subtotal)

    def test_eliminar_reserva(self):
        self.reserva.eliminar()
        self.assertFalse(self.reserva.activa)      

