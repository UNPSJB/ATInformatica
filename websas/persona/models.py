from django.db import models
from safedelete.models import SafeDeleteModel, SOFT_DELETE

class Persona(SafeDeleteModel):
    """ Modelo genérico para la gestión de personas. """
    _safedelete_policy = SOFT_DELETE
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


class Rol(SafeDeleteModel):
    """ Modelo genérico para la gestión de roles de personas. """
    _safedelete_policy = SOFT_DELETE
    TIPO = 0
    ROLNAME = "Rol"

    TIPOS = [
        (0, ROLNAME)
    ]

    tipo = models.PositiveSmallIntegerField(choices=TIPOS)
    persona = models.ForeignKey(
        Persona,
        related_name="roles",
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return "{}".format(self.ROLNAME)
    @property
    def nombre(self):
        return self.persona.nombre

    @property
    def apellido(self):
        return self.persona.apellido
    @property
    def doc(self):
        return self.persona.doc

    @property
    def domicilio(self):
        return self.persona.domicilio

    @property
    def correo(self):
        return self.persona.email

    @property
    def telefono(self):
        return self.persona.telefono

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.tipo = self.__class__.TIPO
        super(Rol, self).save(*args, **kwargs)

    def eliminar(self):
        """ Método para dar de baja una reserva (baja lógica) """
        self.activo = False
        self.save()

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
    ROLNAME = "Técnico"


class Cliente(Rol):
    """ Modelo de rol Técnico. """
    TIPO = 2
    ROLNAME = "Cliente"

class JefeTaller(Rol):
    """ Modelo de rol Técnico. """
    TIPO = 3
    ROLNAME = "Jefe de Taller"
class Gerente(Rol):
    """ Modelo de rol Técnico. """
    TIPO = 4
    ROLNAME = "Gerente"


for Klass in Rol.__subclasses__():
    Rol.register(Klass)
