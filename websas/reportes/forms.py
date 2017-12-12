from django.contrib.auth.forms import forms

FORMATO_FECHA = "%d/%m/%Y"


class ReporteTotalOrdenesForm(forms.Form):
    CHOICES = (
        ("rubro", "Rubro"),
        ("tipo_servicio", "Tipo de servicio"),
        ("cliente", "Cliente"),
        ("tecnico", "Técnico"),
    )
    filtros = forms.ChoiceField(CHOICES, widget=forms.Select(attrs={
        'class': 'form-control chart-input'
    }))

    fecha_ini = forms.DateTimeField(input_formats=[FORMATO_FECHA])
    fecha_fin = forms.DateTimeField(input_formats=[FORMATO_FECHA])

class ReporteProductoForm(forms.Form):
    CHOICES = (
        ("rubro_productos", "Rubro"),
        ("tipo_servicio_productos", "Tipo de servicio"),
    )
    filtros = forms.ChoiceField(CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'
    }))

    fecha_ini = forms.DateTimeField(input_formats=[FORMATO_FECHA])
    fecha_fin = forms.DateTimeField(input_formats=[FORMATO_FECHA])

class ReporteEvolucionFacturacionMensualForm(forms.Form):
    fecha_ini = forms.DateTimeField(input_formats=[FORMATO_FECHA])

class ReporteCargaTrabajoForm(forms.Form):
    CHOICES = (
        ("rubro", "Rubro"),
        ("tecnico", "Técnico"),
    )
    filtros = forms.ChoiceField(CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'
    }))

