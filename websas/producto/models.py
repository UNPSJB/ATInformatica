from django.db import models

# Create your models here.
class Producto(models.Model):

    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)
    marca = models.CharField(max_length=20)
    stock_minimo = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    precio = models.FloatField()
    