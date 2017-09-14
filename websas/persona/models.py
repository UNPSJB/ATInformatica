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

    def __str__(self):
        return "{} {}".format(self.nombre, self.apellido)

class Rol(models.Model):
    rolname = models.CharField(max_length=20, null=True, blank=True)
    persona = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE,
        null=True
    )

class Tecnico(Rol):
    
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.rolname = "Tecnico" 
    

class Cliente(Rol):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.rolname = "Cliente"

class JefeTaller(Rol):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.rolname = "Jefe de Taller"

class Gerente(Rol):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.rolname = "Gerente"