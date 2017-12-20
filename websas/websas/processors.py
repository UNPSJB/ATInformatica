from django.template import loader
from persona.models import Persona, Cliente, Rol
from producto.models import Producto
from orden.models import Equipo, Orden
from rubro.models import Rubro
from servicio.models import TipoServicio
from tarea.models import TipoTarea
from tarifa.models import Tarifa
from usuario.models import Usuario

AYUDA_URLS = {
    # URL origen : URL ayuda destino HTML
    'index': { 'template': 'ayuda/principal.html', 'titulo': 'Pantalla principal' },

    'grupos': { 'template': 'ayuda/grupos.html', 'titulo': 'Control de Acceso' },

    'cliente_listar': { 'template': 'ayuda/clientes.html', 'titulo': 'Listado de clientes' },

    'orden_listar': { 'template': 'ayuda/ordenes.html', 'titulo': 'Listado de órdenes de trabajo' },
    'orden_crear': { 'template': 'ayuda/orden_nueva.html', 'titulo': 'Crear nueva orden de trabajo' },
    'orden_ver': { 'template': 'ayuda/orden_ver.html', 'titulo': 'Detalles de orden de trabajo' },
    'tarea_ver': { 'template': 'ayuda/tarea_ver.html', 'titulo': 'Detalles de la tarea' },

    'equipo_crear': { 'template': 'ayuda/equipo_crear.html', 'titulo': 'Crear un nuevo equipo' },
    'equipo_listar': { 'template': 'ayuda/equipos.html', 'titulo': 'Listado de equipos' },

    'producto_listar': { 'template': 'ayuda/producto_listar.html', 'titulo': 'Listado de productos' },
    'rubro_listar': { 'template': 'ayuda/rubros.html', 'titulo': 'Listado de rubros' },
    'servicio_listar': { 'template': 'ayuda/servicios.html', 'titulo': 'Listado de tipos de servicio' },

    'reportes': { 'template': 'ayuda/reportes.html', 'titulo': 'Reportes' },
    'cantidad_ordenes': { 'template': 'ayuda/reportes.html', 'titulo': 'Reportes' },
    'productos': { 'template': 'ayuda/reportes.html', 'titulo': 'Reportes' },
    'cantidad_productos': { 'template': 'ayuda/reportes.html', 'titulo': 'Reportes' },
    'facturacion_mensual': { 'template': 'ayuda/reportes.html', 'titulo': 'Reportes' },
    'carga_trabajo': { 'template': 'ayuda/reportes.html', 'titulo': 'Reportes' },
    'tarea_mas_realizada': { 'template': 'ayuda/reportes.html', 'titulo': 'Reportes' },
    'tecnico_finalizador': { 'template': 'ayuda/reportes.html', 'titulo': 'Reportes' },
}

def ayuda(request):
    clave = request.resolver_match.url_name

    try:
        template_ayuda = loader.get_template(AYUDA_URLS[clave]['template'])
        titulo = AYUDA_URLS[clave]['titulo']
        return { 'ayuda_pagina': { 'html': template_ayuda.render(), 'titulo': titulo } }
    except:
        pass    
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
        'cant_empleados': Rol.objects.all().exclude(tipo=0).exclude(tipo=2).exclude(tipo=10).distinct('persona'),
        # 'cant_tecnicos': Tecnico.objects.count(),
        # 'cant_jefes': JefeTaller.objects.count(),
        # 'cant_usuarios': Usuario.objects.count(),

        # Workflow
        'cant_productos': Producto.objects.count(),
        'cant_equipos': Equipo.objects.count(),
        'cant_ordenes_abiertas': Orden.objects.filter(cerrada=False).count(),
        'cant_ordenes_cerradas': Orden.objects.filter(cerrada=True).count(),
    }
    return { 'DBINFO': db_info }