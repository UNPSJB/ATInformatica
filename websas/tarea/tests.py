from django.test import TestCase
from .models import Tarea, TipoTarea, TareaPresupuestada, TareaPendiente, TareaRealizada, TareaCancelada
from producto.models import Producto, ReservaStock
from usuario.models import Usuario
from persona.models import Cliente, Tecnico, Persona
from rubro.models import Rubro
from servicio.models import TipoServicio
from orden.models import Orden
from tarifa.models import Tarifa
# Create your tests here.

class TareaTest(TestCase):

    def setUp(self):
        # creamos una orden de trabajo para agregarle tareas
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
        self.descripcion = "Ta todo completamente hecho mierda"

        self.orden = Orden.crear(
            cliente=self.persona.como(Cliente), 
            usuario=self.usuario, 
            tecnico=self.persona.como(Tecnico), 
            rubro=self.rubro,
            equipo=None, 
            tipo_servicio=self.tipo_servicio, 
            descripcion=self.descripcion
        )
        self.orden.save()
        # creamos un producto para reservar stock
        self.producto = Producto(
            nombre="SSD", 
            descripcion="Disco de estado sólido",
            marca="Kingtong",
            stock_minimo=10,
            stock=20,
            precio=600
        )
        self.producto.save()

        # Creamos un tipo de tarea y una tarifa para la creación de la tarea
        self.tipo_tarea = TipoTarea(nombre="Cambio de disco", rubro=self.rubro)
        self.tipo_tarea.save()   
        self.tarifa = Tarifa(tipo_tarea=self.tipo_tarea, tipo_servicio=self.tipo_servicio, precio=300)
        self.tarifa.save()   

        # creamos la tarea
        self.tarea = Tarea.crear(
            tipo_tarea=self.tipo_tarea,
            orden = self.orden,
            observacion="Guardar el disco viejo")
        self.tarea.save()

    def test_estado_inicial(self):
        self.assertTrue(isinstance(self.tarea.estado, TareaPresupuestada))

    def test_reservar_stock(self):
        self.tarea.hacer("reservar_stock", self.producto, 12)
        self.assertTrue(self.producto.stock_reservado == 12)
    
    def test_cancelar_reserva(self):
        # Creamos una reserva para luego probar el método cancelar
        self.tarea.hacer("reservar_stock", self.producto, 12)
        self.assertTrue(self.producto.stock_reservado == 12)

        self.tarea.hacer("cancelar_reserva", self.producto)
        self.assertEqual(self.producto.stock_reservado, 0)



    def test_aceptar(self):
        self.tarea.hacer("aceptar")
        self.assertTrue(isinstance(self.tarea.estado, TareaPendiente))

    def test_finalizar(self):

        # Intentamos finalizar sin haber aceptado
        try:
            self.tarea.hacer("finalizar")
        except Exception as e:
            pass
        self.assertFalse(isinstance(self.tarea.estado, TareaRealizada))
        self.assertTrue(isinstance(self.tarea.estado, TareaPresupuestada))

        # Aceptamos la tarea para poder finalizar 
        self.tarea.hacer("aceptar")
        self.assertTrue(isinstance(self.tarea.estado, TareaPendiente))

        # Finalizamos la tarea
        self.tarea.hacer("finalizar")
        self.assertTrue(isinstance(self.tarea.estado, TareaRealizada))

    def test_finalizar_sin_stock(self):

        self.producto.stock = 0
        self.producto.save()

        self.tarea.hacer("reservar_stock", self.producto, 12)
        self.assertTrue(self.producto.stock_reservado == 12)
        
        # Aceptamos la tarea para poder finalizar 
        self.tarea.hacer("aceptar")
        self.assertTrue(isinstance(self.tarea.estado, TareaPendiente))

        try:
            self.tarea.hacer("finalizar")
        except Exception as e:
            print(str(e))
        
        self.assertTrue(isinstance(self.tarea.estado, TareaPendiente))

        self.producto.stock = 20
        self.producto.save()


        try:
            self.tarea.hacer("finalizar")
        except Exception as e:
            print(str(e))
        
        self.assertTrue(isinstance(self.tarea.estado, TareaRealizada))
        
        # TODO: consultar por que carajo no cambia el stock.
        # self.assertEqual(self.producto.stock, 8)


    def test_cancelar(self):
        # Testeamos que el método cancelar nos devuelva una tarea en estado Cancelada
        # además si había stock reservado debería devolverlo

        # Creamos una reserva para probar
        self.tarea.hacer("reservar_stock", self.producto, 12)
        self.assertTrue(self.producto.stock_reservado == 12)

        # cancelamos y comprobamos el stock reservado
        self.tarea.hacer("cancelar")
        self.assertTrue(isinstance(self.tarea.estado, TareaCancelada))
        self.assertTrue(self.producto.stock_reservado == 0)