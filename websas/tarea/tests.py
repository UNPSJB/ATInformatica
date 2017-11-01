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
        self.orden = Orden.crear(self.usuario, self.persona.como(Cliente), self.persona.como(Tecnico), self.rubro, self.tipo_servicio, self.descripcion)
        self.orden.save()

        self.producto = Producto(
            nombre="SSD", 
            descripcion="Disco de estado sólido",
            marca="Kingtong",
            stock_minimo=10,
            stock=20,
            precio=600
        )
        self.producto.save()
        self.rubro = Rubro(nombre="Notebooks", descripcion="Reparación de notebooks")
        self.rubro.save()
        self.tipo_tarea = TipoTarea(nombre="Cambio de disco", rubro=self.rubro)
        self.tipo_tarea.save()   
        self.tarifa = Tarifa(tipo_tarea=self.tipo_tarea, tipo_servicio=self.tipo_servicio, precio=300)
        self.tarifa.save()       
        self.tarea = Tarea.crear(
            tipo_tarea=self.tipo_tarea,
            orden = self.orden,
            observacion="Guardar el disco viejo")
        self.tarea.save()
        self.reserva = ReservaStock(tarea=self.tarea, producto=self.producto, cantidad=12)
        self.reserva.save()