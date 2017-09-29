from django.db import models

# Create your models here.
class Producto(models.Model):

    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)
    marca = models.CharField(max_length=20)
    stock_minimo = models.IntegerField()
    stock = models.IntegerField()
    precio = models.FloatField()
    