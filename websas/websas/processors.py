from persona.models import Persona, Cliente, Tecnico, JefeTaller, Gerente
from producto.models import Producto
from orden.models import Equipo, Orden
from rubro.models import Rubro
from servicio.models import TipoServicio
from tarea.models import TipoTarea
from tarifa.models import Tarifa
from usuario.models import Usuario

AYUDA_URLS = {
    'index': '/docs/interfaz/principal.html',

    # 'grupos': '/docs/interfaz/usuarios.html',

    # 'tecnico_listar': '/docs/interfaz/tecnicos.html',
    # 'tecnico_crear': '/docs/interfaz/tecnico_nuevo.html',
    # 'tecnico_ver': '/docs/interfaz/tecnico_detalles.html',
    # 'jefe_listar': '/docs/interfaz/jefes.html',
    # 'jefe_crear': '/docs/interfaz/jefe_nuevo.html',
    # 'jefe_ver': '/docs/interfaz/jefe_detalles.html',
    # 'gerente_listar': '/docs/interfaz/gerentes.html',
    # 'gerente_crear': '/docs/interfaz/gerente_nuevo.html',
    # 'gerente_ver': '/docs/interfaz/gerente_detalles.html',

    'cliente_listar': '/docs/interfaz/clientes.html',
    # 'cliente_crear': '/docs/interfaz/cliente_nuevo.html',
    # 'cliente_ver': '/docs/interfaz/cliente_detalles.html',

    # 'orden_crear': '/docs/interfaz/orden_nueva.html',
    'orden_listar': '/docs/interfaz/ordenes.html',
    # 'orden_ver': '/docs/interfaz/orden_detalles.html',    # Esta va a quedar gordita en el manual
    
    # 'equipo_crear': '/docs/interfaz/equipo_nuevo.html',
    'equipo_listar': '/docs/interfaz/equipos.html',
    # 'equipo_ver': '/docs/interfaz/equipo_detalles.html',

    # 'producto_crear': '/docs/interfaz/producto_nueva.html',
    'producto_listar': '/docs/interfaz/productos.html',
    # 'producto_ver': '/docs/interfaz/producto_detalles.html',
    
    # 'rubro_crear': '/docs/interfaz/rubro_nuevo.html',
    'rubro_listar': '/docs/interfaz/rubros.html',
    
    # 'tipo_tarea_crear': '/docs/interfaz/tipo_tarea_nueva.html',
    # 'tipo_tarea_listar': '/docs/interfaz/tipos_tareas.html',

    # 'servicio_crear': '/docs/interfaz/servicio_nuevo.html',
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