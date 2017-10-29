from django.test import TestCase
from .models import Orden, Creada, Diagnosticada, Aceptada, Cerrada, Cancelada
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

    def test_estado_inicial(self):
        # Testeamos que el estado inicial de la orden sea el correcto
        self.assertTrue(isinstance(self.orden.estado, Creada))

    def test_agregar_detalle(self):
        # Creamos una tarifa y una tarea para agregar el detalle
        tipo_tarea = TipoTarea(nombre="Cambio de disco", rubro=self.rubro)
        tipo_tarea.save()
        self.tarea = Tarea(tipo_tarea=tipo_tarea)
        self.tarea.save()
        self.tarifa = Tarifa(tipo_tarea=self.tarea.tipo_tarea, tipo_servicio=self.orden.tipo_servicio, precio=10)
        self.tarifa.save()

        # Agregamos el detalle
        self.orden.agregar_detalle(self.tarea)

        self.assertEqual(self.orden.detalles.all().count(), 1)
        detalle = self.orden.detalles.all().first()
        self.assertEqual(detalle.orden.id, self.orden.id)
        self.assertEqual(detalle.tarea.id, self.tarea.id)
        
        # Probamos que lance excepción si la tarea no es del rubro de la orden
        rubro = Rubro(nombre="Impresoras Fiscales", descripcion="Reparación de impresoras fiscales")
        rubro.save()
        tipo_tarea = TipoTarea(nombre="Limpieza de cabezales", rubro=rubro)
        tipo_tarea.save()
        tarea = Tarea(tipo_tarea=tipo_tarea)
        tarea.save()
        tarifa = Tarifa(tipo_tarea=tipo_tarea, tipo_servicio=self.orden.tipo_servicio, precio=10)
        tarifa.save()
        try:
            self.orden.agregar_detalle(tarea)
        except Exception as e:
            pass
            #print(str(e))
        self.assertFalse(self.orden.detalles.all().count() > 1)

        # Probamos que lance excepcion si no existe tarifa 
        tarifa.delete()
        tarea.tipo_tarea.rubro = self.orden.rubro
        tarea.save()
        try:
            self.orden.agregar_detalle(tarea)
        except Exception as e:
            pass
            #print(str(e))
        self.assertFalse(self.orden.detalles.all().count() > 1)


class EstadoTest(OrdenTest):
    
    def setUp(self):
        super().setUp()
        self.tareas = []
        tipo_tarea = TipoTarea(nombre="Cambio de disco", rubro=self.rubro)
        tipo_tarea.save()
        self.tarea1 = Tarea(tipo_tarea=tipo_tarea)
        self.tarea1.save()
        tipo_tarea = TipoTarea(nombre="Instalacion sistema operativo", rubro=self.orden.rubro)
        tipo_tarea.save()
        self.tarea2 = Tarea(tipo_tarea=tipo_tarea)
        self.tarea2.save()

    def test_agregar_tarea(self):

        # Probamos caso de éxito
        self.orden.estado.agregar_tarea(self.tarea1)
        self.assertEqual(self.orden.tareas.all().count(), 1)
        tarea = self.orden.tareas.all().first()
        self.assertEqual(tarea.id, self.tarea1.id)

        # Probamos que lance excepción si la tarea no es del rubro de la orden
        rubro = Rubro(nombre="Impresoras Fiscales", descripcion="Reparación de impresoras fiscales")
        rubro.save()
        tipo_tarea = TipoTarea(nombre="Limpieza de cabezales", rubro=rubro)
        tipo_tarea.save()
        tarea = Tarea(tipo_tarea=tipo_tarea)
        tarea.save()
        try:
            self.orden.estado.agregar_tarea(tarea)
        except:
            pass
        self.assertFalse(tarea in self.orden.tareas.all())
    

    def test_hacer(self):
        # comprobamos que no tiene tareas
        tareas = self.orden.tareas.all()
        self.assertFalse(tareas)
        
        self.orden.hacer("agregar_tarea", self.tarea1)
        self.assertEqual(self.orden.tareas.all().count(), 1)

    def test_set_col_tareas(self):
        self.tareas.append(self.tarea1)
        self.tareas.append(self.tarea2)

        self.orden.hacer("set_col_tareas", self.tareas)
        self.assertEqual(self.orden.tareas.count(), 2)

    
    def test_cancelar(self):
        # Probamos que pase a cancelada
        self.orden.hacer("cancelar", "Porque se me canta")
        self.assertTrue(isinstance(self.orden.estado, Cancelada))

class TransicionesTest(OrdenTest):

    def setUp(self):
        super().setUp()
        self.tareas = []
        tipo_tarea = TipoTarea(nombre="Cambio de disco", rubro=self.orden.rubro)
        tipo_tarea.save()
        self.tarea1 = Tarea(tipo_tarea=tipo_tarea)
        self.tarea1.save()
        tipo_tarea = TipoTarea(nombre="Instalacion sistema operativo", rubro=self.orden.rubro)
        tipo_tarea.save()
        self.tarea2 = Tarea(tipo_tarea=tipo_tarea)
        self.tarea2.save()
        tipo_tarea = TipoTarea(nombre="Cambio de teclado", rubro=self.orden.rubro)
        tipo_tarea.save()
        self.tarea3 = Tarea(tipo_tarea=tipo_tarea)
        self.tarea3.save()
        self.tareas.append(self.tarea1)
        self.tareas.append(self.tarea2)
        self.tareas.append(self.tarea3)

    def test_trancisiones(self):

        ######################################################
        #                - Estado CREADA - 
        ######################################################

        # Probando el método diagnosticar - debe quedar Diagnosticada
        # Ante lista de tareas vacía no debe transicionar
        tareas = []
        self.orden.hacer("diagnosticar", tareas)
        self.assertFalse(isinstance(self.orden.estado, Diagnosticada))
        self.assertTrue(isinstance(self.orden.estado, Creada))
        self.orden.hacer("diagnosticar", self.tareas)
        self.assertTrue(isinstance(self.orden.estado, Diagnosticada))
    
        ######################################################
        #                - Estado DIAGNOSTICADA - 
        ######################################################

        # Probando que no pueda transicionar si no tiene tareas
        # Removemos a la fuerza las tareas del estado Diagnosticada
        # esta situación no debería ocurrir por lo probado en las lineas anteriores
        [self.orden.estado.tareas.remove(tarea) for tarea in self.orden.tareas.all()]
        self.orden.hacer("aceptar")
        self.assertFalse(isinstance(self.orden.estado, Aceptada))
        self.assertTrue(isinstance(self.orden.estado, Diagnosticada))

        # Agregamos tareas al estado para probar la nueva transicion
        [self.orden.hacer("agregar_tarea", tarea) for tarea in self.tareas]        

        # Probando el método aceptar - debe quedar Aceptada y tener la misma cantidad de tareas
        self.orden.hacer("aceptar")
        self.assertTrue(isinstance(self.orden.estado, Aceptada))
        self.assertEqual(self.orden.tareas.all().count(), 3)

        ######################################################
        #                - Estado ACEPTADA - 
        ######################################################

        # Probando diagnosticar en estado Aceptada - Debe quedar Diagnosticada y tener una tarea mas
        tipo_tarea = TipoTarea(nombre="Cambio de pantalla", rubro=self.orden.rubro)
        tipo_tarea.save()
        tarea4 = Tarea(tipo_tarea=tipo_tarea)
        tarea4.save()
        tareas2 = []
        tareas2.append(tarea4)
        self.orden.hacer("diagnosticar", tareas2)
        self.assertTrue(isinstance(self.orden.estado, Diagnosticada))
        self.assertEqual(self.orden.tareas.all().count(), 4)    

        # Probando el metodo consensuar con solo 3 de las 4 tareas - debe quedar Aceptada y tener 3 tareas
        self.orden.hacer("consensuar", self.tareas)
        # Debe quedar aceptada y consistente la cantidad de tareas
        self.assertTrue(isinstance(self.orden.estado, Aceptada))
        self.assertEqual(self.orden.tareas.all().count(), 3)
        self.assertFalse(tarea4 in self.tareas)

        # Probando el metodo finalizar_tarea
        # Creamos tarifas para probar
        tarifa1 = Tarifa(tipo_tarea=self.tareas[0].tipo_tarea, tipo_servicio=self.orden.tipo_servicio, precio=10)
        tarifa1.save()
        tarifa2 = Tarifa(tipo_tarea=self.tareas[1].tipo_tarea, tipo_servicio=self.orden.tipo_servicio, precio=20)
        tarifa2.save()
        tarifa3 = Tarifa(tipo_tarea=self.tareas[2].tipo_tarea, tipo_servicio=self.orden.tipo_servicio, precio=30)
        tarifa3.save()

        # llamamos a finalizar tarea
        self.orden.hacer("finalizar_tarea", self.orden.tareas.all().first())

        # Al finalizar una tarea se debe crear un detalle y debe haber una tarea menos en el estado
        detalle = self.orden.detalles.get(tarea=self.tareas[0])
        self.assertTrue(detalle)
        self.assertEqual(self.orden.tareas.all().count(), 2)

        # Finalizamos una tarea mas y la proxima deberia cambiar el estado a Cerrada
        self.orden.hacer("finalizar_tarea", self.orden.tareas.all().first())
        self.assertEqual(self.orden.tareas.all().count(), 1)

        # Esta que es la ultima debe cambiar el estado a cerrada
        self.orden.hacer("finalizar_tarea", self.orden.tareas.all().first())
        self.assertTrue(isinstance(self.orden.estado, Cerrada))
