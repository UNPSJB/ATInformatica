from django.db import models
from decimal import Decimal
# Create your models here.
class Tarifa(models.Model):
    tipo_tarea = models.ForeignKey(
        "tarea.TipoTarea", related_name="tarifas",
        on_delete=models.CASCADE
    )
    tipo_servicio = models.ForeignKey(
        "servicio.TipoServicio", related_name="tarifas",
        on_delete=models.CASCADE
    )
    precio = models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0'))

    def actualizar_precio(self, precio):
        """Método para actualizar el precio de una tarifa
        
        Args:
            precio(str): nuevo precio para la tarifa"""
            
        if not precio.isdigit() or int(precio) < 0:
            precio = 0

        self.precio=Decimal(precio)
        self.save()
            
             
    class Meta:
        unique_together = (("tipo_tarea", "tipo_servicio"),)
