from django.contrib.auth.forms import forms
from rubro.models import Rubro
from servicio.models import TipoServicio
from tarea.models import TipoTarea

FORMATO_FECHA = "%d/%m/%Y"


class ReporteTotalOrdenesForm(forms.Form):
    CHOICES = (
        ("rubro", "Rubro"),
        ("tipo_servicio", "Tipo de servicio"),
        # ("cliente", "Cliente"),
        ("tecnico", "Técnico"),
    )
    filtros = forms.ChoiceField(CHOICES, widget=forms.Select(attrs={
        'class': 'form-control chart-input'
    }), label="Criterio:")

    fecha_ini = forms.DateTimeField(input_formats=[FORMATO_FECHA])
    fecha_fin = forms.DateTimeField(input_formats=[FORMATO_FECHA])

class ReporteProductoForm(forms.Form):
    CHOICES = (
        ("rubro", "Rubro"),
        ("tipo_servicio", "Tipo de servicio"),
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
        'class': 'form-control chart-input-carga'
    }))


from django.forms import ModelChoiceField

class TipoServicioChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nombre
class ReporteTareaMasRealizadaForm(forms.Form):
    fecha_ini = forms.DateTimeField(input_formats=[FORMATO_FECHA])
    fecha_fin = forms.DateTimeField(input_formats=[FORMATO_FECHA])

    rubro = forms.ModelChoiceField(
        queryset=Rubro.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }))
    tipo_servicio = TipoServicioChoiceField(
        queryset=TipoServicio.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }))
class TipoTareaChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}: {}".format(obj.rubro.nombre.upper(), obj.nombre)

class ReporteTecnicoFinalizadorForm(forms.Form):
    fecha_ini = forms.DateTimeField(input_formats=[FORMATO_FECHA])
    fecha_fin = forms.DateTimeField(input_formats=[FORMATO_FECHA])

    tipo_servicio = TipoServicioChoiceField(
        queryset=TipoServicio.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={
            'class': 'form-control',
        }))

    tipo_tarea = TipoTareaChoiceField(
        queryset=TipoTarea.objects.all().order_by("rubro__nombre"),
        empty_label=None,
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )

