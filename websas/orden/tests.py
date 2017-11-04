from django.test import TestCase
from .models import Orden
from usuario.models import Usuario
from persona.models import Cliente, Tecnico, Persona
from rubro.models import Rubro
from tarea.models import Tarea, TipoTarea, TareaPresupuestada, TareaPendiente, TareaRealizada, TareaCancelada
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
        self.persona.save()
        self.rubro = Rubro(nombre="Notebooks", descripcion="Reparación de notebooks")
        self.rubro.save()
        self.tipo_servicio = TipoServicio(nombre="Taller", descripcion="Reparación de equipos en taller")
        self.tipo_servicio.save()
        self.descripcion = "Ta todo completamente hecho mierda"
        self.orden = Orden(
            cliente=self.persona.como(Cliente), 
            usuario=self.usuario, 
            tecnico=self.persona.como(Tecnico), 
            rubro=self.rubro,
            equipo=None, 
            tipo_servicio=self.tipo_servicio, 
            descripcion=self.descripcion
        )
        self.orden.save()

    def test_crear(self):
        # Testeamos que haya una orden creada y que sea la nuestra
        self.assertTrue(Orden.objects.all().count(), 1)

    def test_agregar_tarea(self):
        self.tipo_tarea1 = TipoTarea(nombre="Cambio de disco", rubro=self.rubro)
        self.tipo_tarea1.save()
        self.tarifa = Tarifa(tipo_tarea=self.tipo_tarea1, tipo_servicio=self.tipo_servicio, precio=300)
        self.tarifa.save()        
        self.observacion = "Guardar el disco viejo"
       
        # Probamos caso de éxito
        self.orden.agregar_tarea(self.tipo_tarea1, self.observacion)
        self.assertEqual(self.orden.tareas.count(), 1)
        self.assertTrue(self.orden.tareas.get(tipo_tarea=self.tipo_tarea1).estas_presupuestada())

        # Probamos que lance excepción si la tarea no es del rubro de la orden
        rubro = Rubro(nombre="Impresoras Fiscales", descripcion="Reparación de impresoras fiscales")
        rubro.save()
        tipo_tarea = TipoTarea(nombre="Limpieza de cabezales", rubro=rubro)
        tipo_tarea.save()

        try:
            self.orden.agregar_tarea(tipo_tarea, self.observacion)
        except Exception as e:
            self.assertTrue(e)
        
        self.assertEqual(self.orden.tareas.count(), 1)

class OrdenTareasTest(OrdenTest):

    def setUp(self):
        super().setUp()
        self.orden2 = Orden(
            cliente=self.persona.como(Cliente), 
            usuario=self.usuario, 
            tecnico=self.persona.como(Tecnico), 
            rubro=self.rubro,
            equipo=None, 
            tipo_servicio=self.tipo_servicio, 
            descripcion=self.descripcion
        )
        self.orden2.save()
        
        # Creamos un conjunto de tareas para probar las trancisiones
        self.tipo_tarea1 = TipoTarea(nombre="Tarea 1", rubro=self.rubro)
        self.tipo_tarea1.save()
        self.tarifa1 = Tarifa(tipo_tarea=self.tipo_tarea1, tipo_servicio=self.tipo_servicio, precio=300)
        self.tarifa1.save()        
        self.observacion1 = "Tarea 1"

        self.tipo_tarea2 = TipoTarea(nombre="Tarea 2", rubro=self.rubro)
        self.tipo_tarea2.save()
        self.tarifa2 = Tarifa(tipo_tarea=self.tipo_tarea2, tipo_servicio=self.tipo_servicio, precio=1000)
        self.tarifa2.save()        
        self.observacion2 = "Tarea 2"

        self.tipo_tarea3 = TipoTarea(nombre="Tarea 3", rubro=self.rubro)
        self.tipo_tarea3.save()
        self.tarifa3 = Tarifa(tipo_tarea=self.tipo_tarea3, tipo_servicio=self.tipo_servicio, precio=300)
        self.tarifa3.save()        
        self.observacion3 = "Tarea 3"

        self.tipo_tarea4 = TipoTarea(nombre="Tarea 4", rubro=self.rubro)
        self.tipo_tarea4.save()
        self.tarifa4 = Tarifa(tipo_tarea=self.tipo_tarea4, tipo_servicio=self.tipo_servicio, precio=300)
        self.tarifa4.save()        
        self.observacion4 = "Tarea 5"

        self.tipo_tarea5 = TipoTarea(nombre="Tarea 5", rubro=self.rubro)
        self.tipo_tarea5.save()
        self.tarifa5 = Tarifa(tipo_tarea=self.tipo_tarea5, tipo_servicio=self.tipo_servicio, precio=300)
        self.tarifa5.save()        
        self.observacion5 = "Tarea 5"

        self.tipo_tarea6 = TipoTarea(nombre="Tarea 6", rubro=self.rubro)
        self.tipo_tarea6.save()
        self.tarifa6 = Tarifa(tipo_tarea=self.tipo_tarea6, tipo_servicio=self.tipo_servicio, precio=300)
        self.tarifa6.save()        
        self.observacion6 = "Tarea 6"


    def test_aceptar_finalizar(self):
        # Agragamos las tareas con sus distintos tipos
        self.orden2.agregar_tarea(self.tipo_tarea1, self.observacion1)
        self.orden2.agregar_tarea(self.tipo_tarea2, self.observacion2)
        self.orden2.agregar_tarea(self.tipo_tarea3, self.observacion3)
        self.orden2.agregar_tarea(self.tipo_tarea4, self.observacion4)
        self.orden2.agregar_tarea(self.tipo_tarea5, self.observacion5)
        self.orden2.agregar_tarea(self.tipo_tarea6, self.observacion6)

        # Testeamos la propiedad tareas_presupuestadas. 
        self.assertEqual(len(self.orden2.tareas_presupuestadas), 6)
        
        ids_tareas = []
        [ids_tareas.append(tarea.id) for tarea in self.orden2.tareas.all()]

        # Testeamos el método aceptar_tareas y la propiedad tareas_aceptadas
        self.orden2.aceptar_tareas(ids_tareas)
        self.assertEqual(len(self.orden2.tareas_presupuestadas), 0)
        self.assertEqual(len(self.orden2.tareas_pendientes), 6)

        # Testeamos el método finalizar_tareas y la propiedad tareas_realizadas
        self.orden2.finalizar_tareas(ids_tareas)
        self.assertEqual(len(self.orden2.tareas_pendientes), 0)
        self.assertEqual(len(self.orden2.tareas_realizadas), 6)

    def test_presupuestada_cancelar(self):
        # Agragamos las tareas con sus distintos tipos
        self.orden2.agregar_tarea(self.tipo_tarea1, self.observacion1)
        self.orden2.agregar_tarea(self.tipo_tarea2, self.observacion2)
        self.orden2.agregar_tarea(self.tipo_tarea3, self.observacion3)
        self.orden2.agregar_tarea(self.tipo_tarea4, self.observacion4)
        self.orden2.agregar_tarea(self.tipo_tarea5, self.observacion5)
        self.orden2.agregar_tarea(self.tipo_tarea6, self.observacion6)

        # Testeamos la propiedad tareas_presupuestadas. 
        self.assertEqual(len(self.orden2.tareas_presupuestadas), 6)    

        ids_tareas = []
        [ids_tareas.append(tarea.id) for tarea in self.orden2.tareas.all()]

        # Testeamos el método cancelar_tareas y la propiedad tareas_canceladas
        self.orden2.cancelar_tareas(ids_tareas)
        self.assertEqual(len(self.orden2.tareas_presupuestadas), 0)
        self.assertEqual(len(self.orden2.tareas_canceladas), 6)

    def test_cancelar_orden(self):
        # Agragamos las tareas con sus distintos tipos
        self.orden2.agregar_tarea(self.tipo_tarea1, self.observacion1)
        self.orden2.agregar_tarea(self.tipo_tarea2, self.observacion2)
        self.orden2.agregar_tarea(self.tipo_tarea3, self.observacion3)
        self.orden2.agregar_tarea(self.tipo_tarea4, self.observacion4)
        self.orden2.agregar_tarea(self.tipo_tarea5, self.observacion5)
        self.orden2.agregar_tarea(self.tipo_tarea6, self.observacion6)

        # Testeamos la propiedad tareas_presupuestadas. 
        self.assertEqual(len(self.orden2.tareas_presupuestadas), 6)

        self.orden2.cancelar()
        self.assertTrue(self.orden2.cancelada)
        self.assertEqual(len(self.orden2.tareas_canceladas), 6)