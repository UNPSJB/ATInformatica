from django.test import TestCase
from .models import Orden
from usuario.models import Usuario
from persona.models import Cliente, Tecnico, Persona
from rubro.models import Rubro
from tarea.models import Tarea, TipoTarea
from servicio.models import TipoServicio
from tarifa.models import Tarifa
from decimal import Decimal

class OrdenTest(TestCase):
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

    def test_crear(self):
        # Testeamos que haya una orden creada y que sea la nuestra
        self.assertTrue(Orden.objects.all().count(), 1)
        orden = Orden.objects.all().first()
        self.assertEqual(orden.id, self.orden.id)

    def test_agregar_tarea(self):
        self.tipo_tarea = TipoTarea(nombre="Cambio de disco", rubro=self.rubro)
        self.tipo_tarea.save()
        self.tarifa = Tarifa(tipo_tarea=self.tipo_tarea, tipo_servicio=self.tipo_servicio, precio=300)
        self.tarifa.save()        
        self.tarea = Tarea.crear(
            tipo_tarea=self.tipo_tarea,
            orden = self.orden,
            observacion="Guardar el disco viejo")
        self.tarea.save()
        # Probamos caso de éxito
        self.orden.agregar_tarea(self.tarea)
        self.assertEqual(self.orden.tareas.all().count(), 1)
        tarea = self.orden.tareas.all().first()
        self.assertEqual(tarea.id, self.tarea.id)

        # Probamos que lance excepción si la tarea no es del rubro de la orden
        rubro = Rubro(nombre="Impresoras Fiscales", descripcion="Reparación de impresoras fiscales")
        rubro.save()
        tipo_tarea = TipoTarea(nombre="Limpieza de cabezales", rubro=rubro)
        tipo_tarea.save()
        tarea = Tarea(tipo_tarea=tipo_tarea)
        tarea.save()
        try:
            self.orden.agregar_tarea(tarea)
        except:
            pass
        self.assertFalse(tarea in self.orden.tareas.all())
