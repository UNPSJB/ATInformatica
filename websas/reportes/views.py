from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import FormView, TemplateView
# Create your views here.
from django.db.models import Sum, Count, F, Value
from django.db.models.functions import Concat, Upper
from datetime import datetime
from dateutil.relativedelta import relativedelta
from orden.models import Orden
from .forms import ReporteTotalOrdenesForm


FILTROS = {
    'cliente': Concat(Upper(F("cliente__persona__apellido")), Value(', '), F("cliente__persona__nombre")),
    'rubro': F("rubro__nombre"),
    'tipo_servicio': F("tipo_servicio__nombre"),
    'tecnico': Concat(Upper(F("tecnico__persona__apellido")), Value(', '), F("tecnico__persona__nombre")),
}

class ReporteTotalOrdenes(FormView):
    template_name = "reportes/reportes.html"
    form_class = ReporteTotalOrdenesForm


    def get(self, request, *args, **kwargs):

        if(request.is_ajax()):
            return self.ajax_get(request, *args, **kwargs)

        return super().get(request, *args, **kwargs)

    def ajax_get(self, request, *args, **kwargs):
        form = ReporteTotalOrdenesForm(request.GET or None)

        if form.is_valid():

            fecha_ini = form.cleaned_data.get("fecha_ini")
            fecha_fin = form.cleaned_data.get("fecha_fin")
            filtro = FILTROS[form.cleaned_data.get("filtros")]

            ordenes_total = Orden.objects.filter(
                    fecha_fin__range=[fecha_ini, fecha_fin]).values(
                    criterio=filtro).annotate(
                    total=Sum("precio_final"),
                    cantidad=Count("precio_final"))

            # conseguimos la fecha que nos pasaron, pero con un anio menos
            fecha_ini = fecha_ini - relativedelta(years=1)
            fecha_fin = fecha_fin - relativedelta(years=1)

            ordenes_viejas = Orden.objects.filter(
                    fecha_fin__range=[fecha_ini, fecha_fin]).values(
                    criterio=filtro).annotate(
                    total=Sum("precio_final"),
                    cantidad=Count("precio_final"))



            return JsonResponse(
                {
                    "ordenes_total": list(ordenes_total),
                    "ordenes_viejas": list(ordenes_viejas),
                }
            )


        return JsonResponse({})

class ReporteProducto(TemplateView):
    template_name = "reportes/reporte_productos.html"






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
