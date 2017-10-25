from django.test import TestCase
from .models import Orden, Creada, Diagnosticada, Aceptada, Cerrada
from usuario.models import Usuario
from persona.models import Cliente, Tecnico, Persona
from rubro.models import Rubro
from tarea.models import Tarea
from servicio.models import TipoServicio
from tarifa.models import Tarifa
from decimal import Decimal
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
        self.assertTrue(isinstance(self.orden.estado, Creada))

    def test_estados(self):
        # creamos rubros y tareas para las pruebas 
        rubro = Rubro(nombre="Notebooks", descripcion="Reparación de notebooks")
        rubro.save()
        self.orden.rubro = rubro
        self.orden.save()
        tareas = []
        tarea1 = Tarea(nombre="Cambio de disco", rubro=rubro)
        tarea1.save()
        tarea2 = Tarea(nombre="Instalacion sistema operativo", rubro=rubro)
        tarea2.save()
        tarea3 = Tarea(nombre="Cambio de teclado", rubro=rubro)
        tarea3.save()
        tareas.append(tarea1)
        tareas.append(tarea2)
        tareas.append(tarea3)
        
        # Probando el método diagnosticar

        # El .hacer("accion", args) no está funcionando bien
        self.orden.estado.diagnosticar(tareas)
        #self.orden.hacer("diagnosticar", tareas)
        
        # Debe quedar Diagnosticada
        self.assertTrue(isinstance(self.orden.estado, Diagnosticada))
        
        # Probando el método aceptar - debe quedar Aceptada y tener la misma cantidad de tareas
        self.orden.estado.aceptar()
        self.assertTrue(isinstance(self.orden.estado, Aceptada))
        self.assertEqual(self.orden.estado.tareas.all().count(), 3)
        
        
        # Creamos una nueva tarea para probar diagnosticar en Aceptada
        tarea4 = Tarea(nombre="Cambio de pantalla", rubro=rubro)
        tarea4.save()
        tareas2 = []
        tareas2.append(tarea4)
        self.orden.estado.diagnosticar(tareas2)
        # Debe quedar Diagnosticada y tener una tarea mas
        self.assertTrue(isinstance(self.orden.estado, Diagnosticada))
        self.assertEqual(self.orden.estado.tareas.all().count(), 4)
        
        # Probando el metodo consensuar
        self.orden.estado.consensuar(tareas)
        # Debe quedar aceptada y consistente la cantidad de tareas
        self.assertTrue(isinstance(self.orden.estado, Aceptada))
        self.assertEqual(self.orden.estado.tareas.all().count(), 3)


        # Probando el metodo finalizar_tarea
        #
        # Creamos tarifas para probar
        tarifa1 = Tarifa(tarea=tarea1, tipo_servicio=self.orden.tipo_servicio, precio=10)
        tarifa1.save()
        tarifa2 = Tarifa(tarea=tarea2, tipo_servicio=self.orden.tipo_servicio, precio=20)
        tarifa2.save()
        tarifa3 = Tarifa(tarea=tarea3, tipo_servicio=self.orden.tipo_servicio, precio=30)
        tarifa3.save()

        self.orden.estado.finalizar_tarea(self.orden.estado.tareas.all().first())
        # Al finalizar una tarea se debe crear un detalle y debe haber una tarea menos en el estado
        detalle = self.orden.detalles.get(tarea=tarea1)
        self.assertEqual(detalle.precio, tarifa1.precio)
        self.assertEqual(self.orden.estado.tareas.all().count(), 2)

        # Finalizamos una tarea mas y la proxima deberia cambiar el estado a Cerrada
        self.orden.estado.finalizar_tarea(self.orden.estado.tareas.all().first())
        self.assertEqual(self.orden.estado.tareas.all().count(), 1)

        self.orden.estado.finalizar_tarea(self.orden.estado.tareas.all().first())
        self.assertTrue(isinstance(self.orden.estado, Cerrada))

        # Falla el anteriror probamos cerrar a manopla
        # self.orden.estado.cerrar()
        # self.assertTrue(isinstance(self.orden.estado, Cerrada))