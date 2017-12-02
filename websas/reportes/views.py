from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
# Create your views here.
from django.db.models import Sum, F, Value
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
            
            ordenes = Orden.objects.filter(
                fecha_fin__range=[fecha_ini, fecha_fin]).values(
                    propietario=Concat(Upper(F("cliente__persona__apellido")),
                    Value(", "), 
                    F("cliente__persona__nombre"))).annotate(
                    total=Sum("precio_final"))
            
                
            return JsonResponse({"ordenes": list(ordenes)})

        return JsonResponse({})
