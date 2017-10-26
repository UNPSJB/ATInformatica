from django.test import TestCase
from .models import Orden, Creada, Diagnosticada, Aceptada, Cerrada
from usuario.models import Usuario
from persona.models import Cliente, Tecnico, Persona
from rubro.models import Rubro
from tarea.models import Tarea
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
        self.orden = Orden.crear(self.usuario, self.persona.como(Cliente), self.rubro, self.tipo_servicio, self.descripcion)
        self.orden.save()

    def test_crear(self):
        # Testeamos que haya una orden creada y que sea la nuestra
        self.assertTrue(Orden.objects.all().count(), 1)
        orden = Orden.objects.all().first()
        self.assertEqual(orden.id, self.orden.id)

    def test_estado_inicial(self):
        # Testeamos que el estado inicial de la orden sea el correcto
        self.assertTrue(isinstance(self.orden.estado, Creada))

    def test_agregar_detalle(self):
        # Creamos una tarifa y una tarea para agregar el detalle
        self.tarea = Tarea(nombre="Cambio de disco", rubro=self.rubro)
        self.tarea.save()
        self.tarifa = Tarifa(tarea=self.tarea, tipo_servicio=self.orden.tipo_servicio, precio=10)
        self.tarifa.save()

        # Agregamos el detalle
        self.orden.agregar_detalle(self.tarea)

        self.assertEqual(self.orden.detalles.all().count(), 1)
        detalle = self.orden.detalles.all().first()
        self.assertEqual(detalle.orden.id, self.orden.id)
        self.assertEqual(detalle.tarea.id, self.tarea.id)
        self.assertEqual(detalle.precio, self.tarifa.precio)

        # Probamos que lance excepción si la tarea no es del rubro de la orden
        rubro = Rubro(nombre="Impresoras Fiscales", descripcion="Reparación de impresoras fiscales")
        rubro.save()
        tarea = Tarea(nombre="Limpieza de cabezales", rubro=rubro)
        tarea.save()
        tarifa = Tarifa(tarea=tarea, tipo_servicio=self.orden.tipo_servicio, precio=10)
        tarifa.save()
        try:
            self.orden.agregar_detalle(tarea)
        except Exception as e:
            print(str(e))
        self.assertFalse(self.orden.detalles.all().count() > 1)

        # Probamos que lance excepcion si no existe tarifa 
        tarifa.delete()
        tarea.rubro = self.orden.rubro
        tarea.save()
        try:
            self.orden.agregar_detalle(tarea)
        except Exception as e:
            print(str(e))
        self.assertFalse(self.orden.detalles.all().count() > 1)


class EstadosTest(OrdenTest):

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