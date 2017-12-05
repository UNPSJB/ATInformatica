from persona.models import Persona, Cliente, Tecnico, JefeTaller, Gerente
from producto.models import Producto
from orden.models import Equipo, Orden
from rubro.models import Rubro
from servicio.models import TipoServicio
from tarea.models import TipoTarea
from tarifa.models import Tarifa
from usuario.models import Usuario

AYUDA_URLS = {
    # URL origen : URL ayuda destino HTML
    'index': '/docs/interfaz/principal.html',
    'cliente_listar': '/docs/interfaz/clientes.html',
    'orden_listar': '/docs/interfaz/ordenes.html',
    'equipo_listar': '/docs/interfaz/equipos.html',
    'producto_listar': '/docs/interfaz/productos.html',
    'rubro_listar': '/docs/interfaz/rubros.html',
    'servicio_listar': '/docs/interfaz/servicios.html',
}

def ayuda(request):
    clave = request.resolver_match.url_name

    if clave in AYUDA_URLS:
        return { 'ayuda_pagina': AYUDA_URLS[clave] }

    return {}

def websasdbinfo(request):
    db_info = {
        # Tarifario
        'cant_tiposservicio': TipoServicio.objects.count(),
        'cant_rubros': Rubro.objects.count(),
        'cant_tipostarea': TipoTarea.objects.count(),
        'cant_tarifas_0': Tarifa.objects.filter(precio=0).count(),

        # Personas
        'cant_clientes': Cliente.objects.count(),
        'cant_tecnicos': Tecnico.objects.count(),
        'cant_jefes': JefeTaller.objects.count(),
        'cant_usuarios': Usuario.objects.count(),

        # Workflow
        'cant_productos': Producto.objects.count(),
        'cant_equipos': Equipo.objects.count(),
        'cant_ordenes_abiertas': Orden.objects.filter(cerrada=False).count(),
        'cant_ordenes_cerradas': Orden.objects.filter(cerrada=True).count(),
    }
    return { 'DBINFO': db_info }