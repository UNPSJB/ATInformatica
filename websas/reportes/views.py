from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import FormView
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

class ReporteTotalOrdenesClientesRangoTiempo(FormView):
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

            # ordenes_total = Orden.objects.filter(
                # fecha_fin__range=[fecha_ini, fecha_fin]).values(
                    # propietario=Concat(Upper(
                    # F("cliente__persona__apellido")),
                    # Value(", "),
                    # F("cliente__persona__nombre"))).annotate(
                    # total=Sum("precio_final")).annotate(
                    # cantidad=Count("precio_final"))

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


            # ordenes_cantidad_cliente = Orden.objects.filter(
                # fecha_fin__range=[fecha_ini, fecha_fin]).values(
                    # propietario=Concat(Upper(F("cliente__persona__apellido")),
                    # Value(", "),
                    # F("cliente__persona__nombre"))).annotate(
                    # cantidad=Count("precio_final"))

            # ordenes_cantidad_tecnico = Orden.objects.filter(
                # fecha_fin__range=[fecha_ini, fecha_fin]).values(
                    # tecnico_encargado=Concat(Upper(F("tecnico__persona__apellido")),
                    # Value(", "),
                    # F("tecnico__persona__nombre"))).annotate(
                    # total=Count("precio_final"))


            # print(ordenes_total)
            # print(ordenes_cantidad_cliente)
            # print(ordenes_cantidad_tecnico)

            return JsonResponse(
                {
                    "ordenes_total": list(ordenes_total),
                    "ordenes_viejas": list(ordenes_viejas),
                    # "ordenes_cantidad_tecnico": list(ordenes_cantidad_tecnico)
                }
            )


        return JsonResponse({})





 # ReservaStock.objects.deleted_only().exclude(cancelada=True).values(prod=F("producto__nombre"), rubro=F("tarea__orden__rubro__nombre")).annotate(utilizados=Sum("cantidad"))

# ReservaStock.objects.deleted_only().exclude(cancelada=True).values(prod=F("producto__nombre"), rubro=F("tarea__orden__rubro__nombre")).annotate(cantidad=Count("rubro"), total=Sum("precio_unitario"))
