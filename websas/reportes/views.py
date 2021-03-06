from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import FormView, TemplateView, View
# Create your views here.
from django.db.models import Sum, Count, F, Value, FloatField, DecimalField, IntegerField, Case, When
from django.db.models.functions import Concat, Upper, TruncDay, Extract
from datetime import datetime
from decimal import Decimal
from dateutil.relativedelta import relativedelta
from orden.models import Orden
from tarea.models import TareaRealizada
from persona.models import Cliente, Tecnico
from producto.models import ReservaStock
from rubro.models import Rubro
from servicio.models import TipoServicio
from .forms import ReporteTotalOrdenesForm, ReporteProductoForm, ReporteEvolucionFacturacionMensualForm, ReporteCargaTrabajoForm, ReporteTareaMasRealizadaForm, ReporteTecnicoFinalizadorForm

class ReporteTotalOrdenes(FormView):

    FILTROS = {
        'rubro': (Rubro, F("nombre"), lambda r: r.nombre),
        'tipo_servicio': (TipoServicio, F("nombre"), lambda ts: ts.nombre),
        'cliente': (Cliente, Concat(Upper(F("persona__apellido")), Value(', '), F("persona__nombre")), lambda c: "{}, {}".format(c.persona.apellido.upper(), c.persona.nombre)),
        'tecnico': (Tecnico, Concat(Upper(F("persona__apellido")), Value(', '), F("persona__nombre")), lambda t: "{}, {}".format(t.persona.apellido.upper(), t.persona.nombre)),
    }

    template_name = "reportes/reporte_totales.html"
    form_class = ReporteTotalOrdenesForm
    def get(self, request, *args, **kwargs):
        if(request.is_ajax()):
            return self.ajax_get(request, *args, **kwargs)

        return super().get(request, *args, **kwargs)

    def ajax_get(self, request, *args, **kwargs):
        form = self.form_class(request.GET or None)

        if form.is_valid():

            fecha_ini = form.cleaned_data.get("fecha_ini")
            fecha_fin = form.cleaned_data.get("fecha_fin")

            Klass = self.FILTROS[form.cleaned_data.get("filtros")][0]
            criterio = self.FILTROS[form.cleaned_data.get("filtros")][1]
            referencia = self.FILTROS[form.cleaned_data.get("filtros")][2]
            
            query = Klass.objects.values(criterio=criterio).filter(
            ordenes__fecha_fin__range=[fecha_ini, fecha_fin]).annotate(
                total=Case(
                When(
                    ordenes__precio_final__isnull=False,
                    then=F("ordenes__precio_final") 
                ), default=Value(0))).order_by("criterio")

            cache = {}

            for q in query:
                if q["criterio"] not in cache.keys():
                    cache[q["criterio"]] = q["total"]
                    continue
                cache[q["criterio"]] += q["total"]

            for k in Klass.objects.all():
                if referencia(k) not in cache.keys():
                    cache[referencia(k)] = Decimal(0)

            return JsonResponse(
                {
                    "ordenes_total": sorted(list(cache.items()), key=lambda ot: ot[0]),
                }
            )
        return JsonResponse({})

class ReporteCantidadOrdenes(FormView):
    template_name = "reportes/reporte_totales.html"
    form_class = ReporteTotalOrdenesForm

    FILTROS = {
        'rubro': (Rubro, F("nombre")),
        'tipo_servicio': (TipoServicio, F("nombre")),
        'cliente': (Cliente, Concat(Upper(F("persona__apellido")), Value(', '), F("persona__nombre"))),
        'tecnico': (Tecnico, Concat(Upper(F("persona__apellido")), Value(', '), F("persona__nombre"))),
    }

    def get(self, request, *args, **kwargs):
        if(request.is_ajax()):
            return self.ajax_get(request, *args, **kwargs)

        return super().get(request, *args, **kwargs)

    def ajax_get(self, request, *args, **kwargs):
        form = self.form_class(request.GET or None)

        if form.is_valid():

            fecha_ini = form.cleaned_data.get("fecha_ini")
            fecha_fin = form.cleaned_data.get("fecha_fin")

            Klass = self.FILTROS[form.cleaned_data.get("filtros")][0]
            criterio = self.FILTROS[form.cleaned_data.get("filtros")][1]
            
            cantidad_ordenes = Klass.objects.values(
                criterio=criterio).annotate(
                cantidad=Count("ordenes")).order_by("criterio")

            return JsonResponse(
                {
                    "cantidad_ordenes": list(cantidad_ordenes),
                }
            )
        return JsonResponse({})

class ReporteTotalProductos(FormView):
    template_name = "reportes/reporte_productos.html"
    form_class = ReporteProductoForm

    FILTROS = {
        'rubro': (F("tarea__orden__rubro__nombre"), Rubro),
        'tipo_servicio': (F("tarea__orden__tipo_servicio__nombre"), TipoServicio)
    }

    def get(self, request, *args, **kwargs):

        if(request.is_ajax()):
            return self.ajax_get(request, *args, **kwargs)

        return super().get(request, *args, **kwargs)

    def ajax_get(self, request, *args, **kwargs):
        form = self.form_class(request.GET or None)

        if form.is_valid():

            fecha_ini = form.cleaned_data.get("fecha_ini")
            fecha_fin = form.cleaned_data.get("fecha_fin")
            filtro = self.FILTROS[form.cleaned_data.get("filtros")][0]
            Klass = self.FILTROS[form.cleaned_data.get("filtros")][1]


            query = []
            #va queriendo, falta atajar el caso de la instalacion de red,
            #que como nunca se usan repuestos, no aparece ninguna reservado
            #habria que armar un diccionario con ese nombre de criterio,
            #y un Decimal(0)
            for k in Klass.objects.all():
                incidencia = ReservaStock.objects.deleted_only().exclude(
                    cancelada=True).filter(
                    deleted__range=[fecha_ini, fecha_fin]).values(
                    criterio=filtro).annotate(
                    incidencia=Case(
                        When(
                            criterio=k.nombre,
                            then=Sum(F("precio_unitario")*F("cantidad"),
                            output_field=DecimalField())),
                        default=Value(0))).order_by("-incidencia")

                if(k.nombre not in [q["criterio"] for q in incidencia]):
                    query.append({"criterio": k.nombre, "incidencia": Decimal(0)})
                    continue

                query.append(incidencia[0])

            return JsonResponse(
                {
                    "incidencia_productos": sorted(query, key=lambda x: x["criterio"]),
                }
            )


        return JsonResponse({})

class ReporteCantidadProductos(FormView):
    template_name = "reportes/reporte_productos.html"
    form_class = ReporteProductoForm

    FILTROS = {
        'rubro': F("tarea__orden__rubro__nombre"),
        'tipo_servicio': F("tarea__orden__tipo_servicio__nombre"), 
    }

    def get(self, request, *args, **kwargs):

        if(request.is_ajax()):
            return self.ajax_get(request, *args, **kwargs)

        return super().get(request, *args, **kwargs)

    def ajax_get(self, request, *args, **kwargs):
        form = self.form_class(request.GET or None)

        if form.is_valid():

            fecha_ini = form.cleaned_data.get("fecha_ini")
            fecha_fin = form.cleaned_data.get("fecha_fin")
            filtro = self.FILTROS[form.cleaned_data.get("filtros")]

            cantidad_productos = ReservaStock.objects.deleted_only().exclude(
                cancelada=True).values(
                criterio=filtro).order_by(
                "criterio").annotate(cantidad=Sum("cantidad"))


            return JsonResponse(
                {
                    "cantidad_productos": list(cantidad_productos),
                }
            )


        return JsonResponse({})

class ReporteEvolucionFacturacionMensual(View):

    form_class = ReporteEvolucionFacturacionMensualForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET or None)
        if form.is_valid():
            fecha = form.cleaned_data.get("fecha_ini")

            facturacion = Orden.objects.filter(
                fecha_fin__year=fecha.year,
                fecha_fin__month=fecha.month).annotate(
                dia=Extract("fecha_fin", "day")).values(
                "dia").annotate(c=Count("dia")).annotate(
                total_dia=Sum("precio_final")).values(
                "dia", "total_dia").order_by("dia")

            days = {ot["dia"]:ot["total_dia"] for ot in facturacion}
            query = {}

            for day in range(1, fecha.day+1):
                if day not in days.keys():
                    query[day] = Decimal()
                    continue
                query[day] = days[day]

            return JsonResponse({
                "facturacion": sorted(list(query.items()), key=lambda x: x[0])
            })
        return JsonResponse({})


class ReporteCargaTrabajoTecnico(View):
    form_class = ReporteCargaTrabajoForm
    FILTROS = {
        'rubro': F("rubro__nombre"),
        'tecnico': Concat(Upper(F("tecnico__persona__apellido")), Value(', '), F("tecnico__persona__nombre")),
    }

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET or None)

        if form.is_valid():
            filtro = self.FILTROS[form.cleaned_data.get("filtros")]

            carga_trabajo = Orden.objects.exclude(
                    cerrada=True
                    ).exclude(
                        cancelada=True
                    ).values(
                        criterio=filtro
                    ).annotate(cantidad_ots_abiertas=Count('criterio'))

            return JsonResponse(
                {
                    "carga_trabajo": list(carga_trabajo),
                }
            )

        return JsonResponse({})

class ReporteTareaMasRealizada(TemplateView):
    template_name = "reportes/reporte_tarea_mas_realizada.html"
    
    def get_context_data(self, **kwargs):
        context = super(ReporteTareaMasRealizada, self).get_context_data(**kwargs)
        context["form"] = ReporteTareaMasRealizadaForm()
        return context
    
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return self.ajax_get(request, *args, **kwargs)

        return super().get(request, *args, **kwargs)

    def ajax_get(self, request, *args, **kwargs):
        form = ReporteTareaMasRealizadaForm(request.GET or None)
        if form.is_valid():
            
            rubro = form.cleaned_data.get("rubro")
            tipo_servicio = form.cleaned_data.get("tipo_servicio")
            fecha_ini = form.cleaned_data.get("fecha_ini")
            fecha_fin = form.cleaned_data.get("fecha_fin")
            query = TareaRealizada.objects.filter(
            tarea__orden__rubro=rubro, 
            tarea__orden__tipo_servicio=tipo_servicio, 
            tarea__orden__fecha_fin__range=[fecha_ini, fecha_fin]).values(rubro=F("tarea__orden__rubro__nombre"), tipo_servicio=F("tarea__orden__tipo_servicio__nombre"), tipo_tarea=F("tarea__tipo_tarea__nombre")).order_by("rubro", "tipo_servicio", "tipo_tarea").annotate(cant=Count("tipo_tarea")).values("tipo_tarea", "cant")

            return JsonResponse({
                "tarea_mas_realizada": list(query), 
            })
            
        return JsonResponse({})

class ReporteTecnicoFinalizador(TemplateView):
    template_name = "reportes/reporte_tecnico_finalizador.html"

    def get_context_data(self, **kwargs):
        context = super(ReporteTecnicoFinalizador, self).get_context_data(**kwargs)
        context["form"] = ReporteTecnicoFinalizadorForm()
        return context

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            return self.ajax_get(request, *args, **kwargs)

        return super().get(request, *args, **kwargs)
    def ajax_get(self, request, *args, **kwargs):
        form = ReporteTecnicoFinalizadorForm(request.GET or None)

        if form.is_valid():
            fecha_ini = form.cleaned_data.get("fecha_ini")
            fecha_fin = form.cleaned_data.get("fecha_fin")
            tipo_servicio = form.cleaned_data.get("tipo_servicio")
            tipo_tarea = form.cleaned_data.get("tipo_tarea")

            query = TareaRealizada.objects.filter(tarea__orden__fecha_fin__range=[fecha_ini, fecha_fin], tarea__orden__tipo_servicio=tipo_servicio, tarea__tipo_tarea=tipo_tarea).values(tipo_tarea=F("tarea__tipo_tarea__nombre"), tecnico=F("usuario__username")).annotate(cantidad=Count("tipo_tarea")).order_by("tipo_tarea", "-cantidad")

            return JsonResponse({
                "tecnico_finalizador": list(query)
            })

        return JsonResponse({})