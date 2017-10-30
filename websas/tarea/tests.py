from django.test import TestCase
from .models import Tarea, TipoTarea, TareaPresupuestada, TareaPendiente, TareaRealizada, TareaCancelada
from producto.models import Producto
from rubro.models import Rubro
# Create your tests here.

class TareaTest(TestCase):

    def setUp(self):
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
        self.tarea = Tarea.crear(
            tipo_tarea=self.tipo_tarea, 
            producto=self.producto, 
            cantidad=1, 
            observacion="Guardar el disco viejo")
        self.tarea.save()

    def test_estado_inicial(self):
        self.assertTrue(isinstance(self.tarea.estado, TareaPresupuestada))

    def test_transiciones(self):
        # Aceptar 
        self.tarea.hacer("aceptar")
        self.assertTrue(isinstance(self.tarea.estado, TareaPendiente))
        
        # Realizar
        self.tarea.hacer("realizar")
        self.assertTrue(isinstance(self.tarea.estado, TareaRealizada))

        # Cancelar
        self.tarea.hacer("cancelar")
        self.assertTrue(isinstance(self.tarea.estado, TareaCancelada))
