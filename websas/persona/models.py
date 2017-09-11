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

class Rol(models.Model):
    persona = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE,
        null=True
    )

class Tecnico(Rol):

    class Meta:
        permissions = (
            ('p1','Permiso Tecnico'),
        )
    

class Cliente(Rol):
    pass