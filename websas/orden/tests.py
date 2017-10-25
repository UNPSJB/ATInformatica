from django.test import TestCase
from .models import Orden, Creada
from usuario.models import Usuario
from persona.models import Cliente, Tecnico, Persona
from rubro.models import Rubro
from servicio.models import TipoServicio

# Create your tests here.
class OrdenTest(TestCase):
    def setUp(self):
        
        persona = Persona(
            nombre="Alguien",
            apellido="Alguien",
            doc="123321123",
            domicilio="cale213",
            email="l@l.com"
        )
        persona.save()
        persona.agregar_rol(Tecnico())
        persona.agregar_rol(Cliente())
        usuario = Usuario.objects.crear_usuario(username="Tecnico1", password="Tecnico1", persona=persona)
        persona.agregar_rol(Usuario())
        persona.save
        rubro = Rubro(nombre="Notebooks", descripcion="Reparación de notebooks")
        rubro.save()
        tipo_servicio = TipoServicio(nombre="Taller", descripcion="Reparación de equipos en taller")
        tipo_servicio.save()
        descripcion = "Ta todo completamente hecho mierda"
        self.orden = Orden.crear(usuario, persona.como(Cliente), rubro, tipo_servicio, descripcion)
        self.orden.save()

    def test_estado_inicial(self):
        estado = self.orden.estado
        print(estado)
        self.assertTrue(isinstance(estado, Creada))

    