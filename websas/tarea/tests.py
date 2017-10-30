from django.test import TestCase
from .models import Tarea, TipoTarea, TareaPresupuestada, TareaEsperaRepuestos, TareaPendiente, TareaRealizada, TareaCancelada
from producto.models import Producto, ReservaStock
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
            observacion="Guardar el disco viejo")
        self.tarea.save()
        self.reserva = ReservaStock(tarea=self.tarea, producto=self.producto, cantidad=12)
        self.reserva.save()

    def test_estado_inicial(self):
        self.assertTrue(isinstance(self.tarea.estado, TareaPresupuestada))


    def test_transiciones(self):
        # Casos de éxito en las transiciones de estados de la tarea
        # Aceptar 
        self.tarea.hacer("aceptar")
        self.assertTrue(isinstance(self.tarea.estado, TareaPendiente))

        # Realizar
        self.tarea.hacer("realizar")
        self.assertTrue(isinstance(self.tarea.estado, TareaRealizada))

        # Cancelar
        self.tarea.hacer("cancelar")
        self.assertTrue(isinstance(self.tarea.estado, TareaCancelada))

class TareaStockTest(TestCase):
    # Test del comportamiento de las transiciones en relacion al stock de productos

    def setUp(self):
        # Creamos un producto con stock 0 y una reserva de 2 unidades
        self.producto = Producto(
            nombre="Ram DDR 4", 
            descripcion="Memoria Ram DDR 4",
            marca="Kingtong",
            stock_minimo=10,
            stock=0,
            precio=600
        )
        self.producto.save()
        self.rubro = Rubro(nombre="Notebooks", descripcion="Reparación de notebooks")
        self.rubro.save()
        self.tipo_tarea = TipoTarea(nombre="Cambio de disco", rubro=self.rubro)
        self.tipo_tarea.save()        
        self.tarea = Tarea.crear(
            tipo_tarea=self.tipo_tarea,
            observacion="Guardar el disco viejo")
        self.tarea.save()
        self.reserva = ReservaStock(tarea=self.tarea, producto=self.producto, cantidad=2)
        self.reserva.save()

    def test_tarea_stock(self):

        # La tarea ahora tiene 2 reservas de las cuales esta ultima no tiene repuestos
        self.tarea.hacer("aceptar")
        self.assertFalse(isinstance(self.tarea.estado, TareaPendiente))
        self.assertTrue(isinstance(self.tarea.estado, TareaEsperaRepuestos))

        # Llamamos a desbloquear para probar que continue en estado TareaEsperaRepuestos
        self.tarea.hacer("desbloquear")
        self.assertFalse(isinstance(self.tarea.estado, TareaPendiente))
        self.assertTrue(isinstance(self.tarea.estado, TareaEsperaRepuestos))

        # Incrementamos el stock del producto y probamos que ahora si se pueda desbloquear
        self.producto.stock = 2
        self.producto.save()

        self.tarea.hacer("desbloquear")
        self.assertTrue(isinstance(self.tarea.estado, TareaPendiente))

        # TODO: Revisar bien - puede ser un tema de la base de datos de test
        # Pareciera ser que hace lo que debe en [método usar_repuestos]
        reserva = self.tarea.reservas.get(pk=self.reserva.id)
        # print("Stock de la reserva {}, antes = {}".format(self.producto.id, str(self.producto.stock)))
        self.tarea.hacer("realizar")
        self.assertTrue(isinstance(self.tarea.estado, TareaRealizada))
        # self.assertEqual()
        # print("Stock de la reserva {}, despues = {} activa {}".format(self.producto.id, str(reserva.producto.stock), reserva.activa))
       