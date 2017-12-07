from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
# Create your views here.
from django.db.models import Sum, Count, F, Value
from django.db.models.functions import Concat, Upper
from datetime import datetime

from orden.models import Orden
from .forms import ReporteTotalOrdenesClientesRangoTiempoForm


class ReporteTotalOrdenesClientesRangoTiempo(TemplateView):
    template_name = "reportes/reportes.html"


    def get(self, request, *args, **kwargs):

        if(request.is_ajax()):
            return self.ajax_get(request, *args, **kwargs)

        return super().get(request, *args, **kwargs)

    def ajax_get(self, request, *args, **kwargs):        
        form = ReporteTotalOrdenesClientesRangoTiempoForm(request.GET or None)

        if form.is_valid():
            
            fecha_ini = form.cleaned_data.get("fecha_ini")
            fecha_fin = form.cleaned_data.get("fecha_fin")
            
            ordenes_total = Orden.objects.filter(
                fecha_fin__range=[fecha_ini, fecha_fin]).values(
                    propietario=Concat(Upper(F("cliente__persona__apellido")),
                    Value(", "), 
                    F("cliente__persona__nombre"))).annotate(
                    total=Sum("precio_final"))
            
            ordenes_cantidad_cliente = Orden.objects.filter(
                fecha_fin__range=[fecha_ini, fecha_fin]).values(
                    propietario=Concat(Upper(F("cliente__persona__apellido")),
                    Value(", "), 
                    F("cliente__persona__nombre"))).annotate(
                    total=Count("precio_final"))

            ordenes_cantidad_tecnico = Orden.objects.filter(
                fecha_fin__range=[fecha_ini, fecha_fin]).values(
                    creador=Concat(Upper(F("tecnico__persona__apellido")),
                    Value(", "), 
                    F("tecnico__persona__nombre"))).annotate(
                    total=Count("precio_final"))


            print(ordenes_total)
            print(ordenes_cantidad_cliente)
            print(ordenes_cantidad_tecnico)
                
            return JsonResponse(
                {
                    "ordenes_total": list(ordenes_total),
                    "ordenes_cantidad_cliente": list(ordenes_cantidad_cliente),
                    "ordenes_cantidad_tecnico": list(ordenes_cantidad_tecnico)
                }
            )


        return JsonResponse({})
