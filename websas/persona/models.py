from django.db import models

# Create your models here.
class Persona(models.Model):
    TIPO_DOC = (
        ('DU', 'DNI'),
        ('CL', 'CUIL'),
        ('CT', 'CUIT'),
    )
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    tipo_doc = models.CharField(max_length=2, choices=TIPO_DOC, default='DU')
    doc = models.CharField(max_length=20, unique = True)
    domicilio = models.TextField()
    email = models.EmailField()
    telefono = models.CharField(max_length=15)

    class Meta:
        abstract = True

class Tecnico(Persona):
    pass    
    

class Cliente(Persona):
    pass