from django.db import models

class Persona(models.Model):
    """ Modelo genérico para la gestión de personas. """
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

    def get_nombre_completo(self):
        return "{} {}".format(self.nombre, self.apellido)

    def como(self, Klass):
        """ Retorna una instancia de un rol asociado a una persona con la ayuda del método 
        related de la clase Rol.
        
        Args
            Klass (string): nombre de una subclase de Rol
        Returns
            instancia de alguna subclase de Rol
        """
        return self.roles.get(tipo=Klass.TIPO).related()

    def agregar_rol(self, rol):
        """ Agrega un rol a una persona.
        
        **Args:**
            - rol (string): rol
        """
        if not self.sos(rol.__class__):
            rol.persona = self
            rol.save()

    def roles_related(self):
        """ Retorna la colección de roles asociados a una persona. """
        return [rol.related() for rol in self.roles.all()]

    def sos(self, Klass):
        """ Recibe una subclase de rol y retorna True si la persona está asociada y False si no.
        
        **Args:**    
            - Klass (string): subclase de Rol
        **Returns:**
            - bool 
        """
        return any([isinstance(rol, Klass) for rol in self.roles_related()])


class Rol(models.Model):
    """ Modelo genérico para la gestión de roles de personas. """
    TIPO = 0
    TIPOS = [
        (0, "rol")
    ]
    tipo = models.PositiveSmallIntegerField(choices=TIPOS)
    rolname = models.CharField(max_length=20, null=True, blank=True)
    persona = models.ForeignKey(
        Persona,
        related_name="roles",
        on_delete=models.CASCADE,
        null=True
    )

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.tipo = self.__class__.TIPO
        super(Rol, self).save(*args, **kwargs)
        

    def related(self):
        """ Retorna una instancia de una subclase de Rol """
        return self.__class__ != Rol and self or getattr(self, self.get_tipo_display())

    @classmethod
    def register(cls, klass):
        """ Método de clase para registrar TIPOS """
        cls.TIPOS.append((klass.TIPO, klass.__name__.lower()))

class Tecnico(Rol):
    """ Modelo de rol Técnico. """
    TIPO = 1
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.rolname = "Tecnico" 
    

class Cliente(Rol):
    """ Modelo de rol Técnico. """
    TIPO = 2

    def ordenes(self, estado):
        return self.ordenes.filter(isinstance(self.ordenes.estado, estado))

class JefeTaller(Rol):
    """ Modelo de rol Técnico. """
    TIPO = 3

class Gerente(Rol):
    """ Modelo de rol Técnico. """
    TIPO = 4

for Klass in Rol.__subclasses__():
    Rol.register(Klass)