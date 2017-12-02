from django.contrib.auth.forms import forms

class ReporteTotalOrdenesClientesRangoTiempoForm(forms.Form):
    fecha_ini = forms.DateTimeField(input_formats=["%d/%m/%Y"])
    fecha_fin = forms.DateTimeField(input_formats=["%d/%m/%Y"])
