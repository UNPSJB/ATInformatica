from django.contrib.auth.forms import forms

FORMATO_FECHA = "%d/%m/%Y"

class ReporteTotalOrdenesClientesRangoTiempoForm(forms.Form):
    fecha_ini = forms.DateTimeField(input_formats=[FORMATO_FECHA])
    fecha_fin = forms.DateTimeField(input_formats=[FORMATO_FECHA])
