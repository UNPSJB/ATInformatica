from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
from django.db.models import Sum, F, Value
from django.db.models.functions import Concat, Upper

from orden.models import Orden


class Reportes(TemplateView):
    template_name = "reportes/reportes.html"


    def get(self, request, *args, **kwargs):
        total_ordenes_por_cliente = Orden.objects.values(
            propietario=Concat(Upper(F("cliente__persona__apellido")),
                               Value(", "),
                               F("cliente__persona__nombre"))).annotate(
                               total=Sum("precio_final"))

        return super().get(request, *args, **kwargs)
