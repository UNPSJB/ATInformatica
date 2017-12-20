from django.test import TestCase
from .models import Persona, Rol, Cliente, Tecnico, JefeTaller, Gerente
from orden.models import Orden

class Persona1erTest(TestCase):
    def test_numero_elementos(self):
        self.assertEqual(0, len(Persona.objects.all()))

class Persona2doTest(TestCase):
    fixtures = ['persona/fixtures.json']

    def test_numero_elementos(self):
        """
        Comprobamos que se han cargado las fixtures
        """
        print(Persona.objects.count())
        self.assertEqual(1520, len(Persona.objects.all()))
    

# 
# TODO: metodos para testear y armado de los casos de prueba 
# 
# en Persona:   1) como(self, Klass);  
#               2) agregar_rol(self, rol)
#               3) roles_related()
#               4) eliminar_rol(self, rol)
#               5) sos(self, Klass)
# 
# en Rol:       1) related()
#               2) register
# 
# ############################################################
# 
# ver el tema de las propiedades y los templates
# 
    

# Create your tests here.

# class PersonasTest(TestCase):
#     def setUp(self):
#         self.persona = Persona(
#             nombre="Alguien",
#             apellido="Alguien",
#             doc="123321123",
#             domicilio="cale213",
#             email="l@l.com"
#         )
#         self.persona.save()

#     def test_sos(self):
#         cliente = Cliente(persona=self.persona)
#         cliente.save()
#         self.assertTrue(self.persona.sos(Cliente)) 

#     def test_agregar_rol(self):
#         self.persona.agregar_rol(Tecnico())
#         es_tecnico = self.persona.sos(Tecnico)
#         self.assertTrue(es_tecnico)

#         self.persona.agregar_rol(Gerente())
#         self.assertTrue(self.persona.sos(Gerente))
    
#     def test_como(self):
#         self.persona.agregar_rol(Tecnico())
#         clase = self.persona.como(Tecnico)
#         self.assertEqual(clase.__class__.__name__,"Tecnico")
        
# class ClienteTest(PersonasTest):
#     def setUp(self):
#         super().setUp()



