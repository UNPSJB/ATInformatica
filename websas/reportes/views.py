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
from producto.models import ReservaStock
from .forms import ReporteTotalOrdenesForm, ReporteProductoForm, ReporteEvolucionFacturacionMensualForm, ReporteCargaTrabajoForm


FILTROS = {
    'cliente': Concat(Upper(F("cliente__persona__apellido")), Value(', '), F("cliente__persona__nombre")),
    'rubro': F("rubro__nombre"),
    'tipo_servicio': F("tipo_servicio__nombre"),
    'tecnico': Concat(Upper(F("tecnico__persona__apellido")), Value(', '), F("tecnico__persona__nombre")),
    'rubro_productos': (F("tarea__orden__rubro__nombre"), F("rubro__nombre")),
    'tipo_servicio_productos': (F("tarea__orden__tipo_servicio__nombre"), F("tipo_servicio__nombre")),
}

class ReporteTotalOrdenes(FormView):
    template_name = "reportes/reporte_totales.html"
    form_class = ReporteTotalOrdenesForm

    @staticmethod
    def get_query(criteria, date_start, date_end):
        """Metodo estatico que devuelve la query asi se lo puede reusar desde otra view"""
        #
        # esta query tiene que devolver la cantidad de plata se recaudo
        # durante un rango de tiempo con cada filtro, pero si no se recaudo
        # nada, que devuelve 0 de total y 0 de cantidad
        #
        ots = Orden.objects.values(criterio=criteria).annotate(
            total=Case(
                When(fecha_fin__range=[date_start, date_end],
                     then=F("precio_final")),
                default=Value(0), output_field=DecimalField()
            )).values("criterio", "total").order_by("criterio", "-precio_final")

        cache = {}
        for ot in ots:
            if ot["criterio"] not in cache.keys():
                cache[ot["criterio"]] = ot["total"]
            cache[ot["criterio"]] += ot["total"]
        return cache.items()


        # return Orden.objects.filter(
                    # fecha_fin__range=[date_start, date_end]).values(
                    # criterio=criteria).annotate(
                    # cantidad=Count("criterio")
                    # ).annotate(hay=Case(
                    # When(cantidad__isnull=False, then=F("cantidad")
                    # ), default=Value(0))).annotate(
                    # total=Sum("precio_final")).order_by("criterio")


    def get(self, request, *args, **kwargs):
        if(request.is_ajax()):
            return self.ajax_get(request, *args, **kwargs)

        return super().get(request, *args, **kwargs)

    def ajax_get(self, request, *args, **kwargs):
        form = self.form_class(request.GET or None)

        if form.is_valid():

            fecha_ini = form.cleaned_data.get("fecha_ini")
            fecha_fin = form.cleaned_data.get("fecha_fin")
            filtro = FILTROS[form.cleaned_data.get("filtros")]

            ordenes_total = ReporteTotalOrdenes.get_query(filtro, fecha_ini, fecha_fin)

            return JsonResponse(
                {
                    "ordenes_total": list(ordenes_total),
                }
            )
        return JsonResponse({})

class ReporteCantidadOrdenes(FormView):
    template_name = "reportes/reporte_totales.html"
    form_class = ReporteTotalOrdenesForm

    @staticmethod
    def get_query(criteria, date_start, date_end):
        """Metodo estatico que devuelve la query asi se lo puede reusar desde otra view"""
        #
        # esta query tiene que devolver la cantidad de plata se recaudo
        # durante un rango de tiempo con cada filtro, pero si no se recaudo
        # nada, que devuelve 0 de total y 0 de cantidad
        #
        ots = Orden.objects.values(criterio=criteria).annotate(
            cantidad=Case(
                When(fecha_fin__range=[date_start, date_end],
                     then=Count("criterio")),
                default=Value(0), output_field=DecimalField()
            )).values("criterio", "cantidad").order_by("criterio")

        cache = {}
        for ot in ots:
            if ot["criterio"] not in cache.keys():
                cache[ot["criterio"]] = ot["cantidad"]
            cache[ot["criterio"]] += ot["cantidad"]
        return cache.items()

    def get(self, request, *args, **kwargs):
        if(request.is_ajax()):
            return self.ajax_get(request, *args, **kwargs)

        return super().get(request, *args, **kwargs)

    def ajax_get(self, request, *args, **kwargs):
        form = self.form_class(request.GET or None)

        if form.is_valid():

            fecha_ini = form.cleaned_data.get("fecha_ini")
            fecha_fin = form.cleaned_data.get("fecha_fin")
            filtro = FILTROS[form.cleaned_data.get("filtros")]

            ordenes_total = ReporteCantidadOrdenes.get_query(filtro, fecha_ini, fecha_fin)

            return JsonResponse(
                {
                    "cantidad_ordenes": list(ordenes_total),
                }
            )
        return JsonResponse({})

class ReporteProducto(FormView):
    template_name = "reportes/reporte_productos.html"
    form_class = ReporteProductoForm

    def get(self, request, *args, **kwargs):

        if(request.is_ajax()):
            return self.ajax_get(request, *args, **kwargs)

        return super().get(request, *args, **kwargs)

    def ajax_get(self, request, *args, **kwargs):
        form = self.form_class(request.GET or None)

        if form.is_valid():

            fecha_ini = form.cleaned_data.get("fecha_ini")
            fecha_fin = form.cleaned_data.get("fecha_fin")
            filtro = FILTROS[form.cleaned_data.get("filtros")][0]

            incidencia_productos = ReservaStock.objects.deleted_only().exclude(
                cancelada=True).values(
                criterio=filtro,
                prod=F("producto__nombre")).order_by("criterio").annotate(
                total_utilizado=Sum("cantidad"), total_recaudado=
                Sum(F("precio_unitario")* F("cantidad"),
                output_field=FloatField()))

            total_facturado = ReporteTotalOrdenes.get_query(filtro, fecha_ini, fecha_fin)

            return JsonResponse(
                {
                    "incidencia_productos": list(incidencia_productos),
                    "total_facturado": list(total_facturado),
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

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.GET or None)
        print(form)

        if form.is_valid():
            filtro = FILTROS[form.cleaned_data.get("filtros")]

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
 # ReservaStock.objects.deleted_only().exclude(cancelada=True).values(prod=F("producto__nombre"), rubro=F("tarea__orden__rubro__nombre")).annotate(utilizados=Sum("cantidad"))

# ReservaStock.objects.deleted_only().exclude(cancelada=True).values(prod=F("producto__nombre"), rubro=F("tarea__orden__rubro__nombre")).annotate(cantidad=Count("rubro"), total=Sum("precio_unitario"))



#esta es la que va
# ReservaStock.objects.deleted_only().exclude(cancelada=True).values(rubro=F("tarea__orden__rubro__nombre"), prod=F("producto__nombre")).order_by("rubro").annotate(total_utilizado=Sum("cantidad"), total_recaudado=Sum(F("precio_unitario")* F("cantidad"), output_field=FloatField()))

# TareaRealizada.objects.values(tipo_tarea=F("tarea__tipo_tarea__nombre"), tecnico=F("usuario__username")).annotate(cantidad=Count("tipo_tarea")).order_by("tipo_tarea")

# cache = {}
# for q in query:
    # if q["tipo_tarea"] not in cache.keys():
        # cache[q["tipo_tarea"]] = (q["tecnico"], q["cantidad"])


# esta es la de rdpys pagadas por ots canceladas
# TareaRealizada.objects.filter(tarea__tipo_tarea__nombre__icontains="rdyp", tarea__orden__cancelada=True).annotate(otras_tareas=Count(F("tarea__orden__tareas"))).filter(otras_tareas=1).annotate(cantidad=Count("tarea__orden__rubro__nombre"))


# Carga de Trabajo por Técnico (Cantidad de OTs abiertas en el momento)
# 
# Orden.objects.exclude(cerrada=True).exclude(cancelada=True).values(criterio=filtro).annotate(cantidad_ots_abiertas=Count('criterio'))
