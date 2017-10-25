from django.test import TestCase
from .models import Persona, Rol, Cliente, Tecnico, JefeTaller
# Create your tests here.

class PersonasTest(TestCase):
    def setUp(self):
        self.persona = Persona(
            nombre="Alguien",
            apellido="Alguien",
            doc="123321123",
            domicilio="cale213",
            email="l@l.com"
        )
        self.persona.save()

    def test_sos(self):
        cliente = Cliente(persona=self.persona)
        cliente.save()
        self.assertTrue(self.persona.sos(Cliente)) 

    def test_agregar_rol(self):
        self.persona.agregar_rol(Tecnico())
        es_tecnico = self.persona.sos(Tecnico)
        self.assertTrue(es_tecnico)
    
    def test_como(self):
        self.persona.agregar_rol(Tecnico())
        clase = self.persona.como(Tecnico)
        self.assertEqual(clase.__class__.__name__,"Tecnico")
        
    # def test_roles_related(self):
    #     self.persona.agregar_rol(Tecnico())
    #     self.persona.agregar_rol(JefeTaller())
    #     roles = self.persona.roles_related()
    #     self.assertEqual(roles, [Tecnico(), JefeTaller()])

