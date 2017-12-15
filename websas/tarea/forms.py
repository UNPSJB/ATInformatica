from django import forms
from .models import TipoTarea
from producto.models import ReservaStock
from tarea.models import TipoTarea
class TipoTareaForm(forms.ModelForm):

    class Meta:
        model = TipoTarea
        fields = [
            'nombre',
            'descripcion',
        ]
        labels = {
            'nombre':'Nombre',
            'descripcion':'Descripción',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'descripcion': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
        }

    def clean_nombre(self):
        data = self.cleaned_data.get("nombre")
        if(data.strip().lower() == TipoTarea.RDYP):
            raise forms.ValidationError("No se puede crear un tipo de tarea de nombre 'RDyP'")

        return data

    def save(self, rubro):
        self.instance.rubro = rubro
        self.instance.save()

class ReservaForm(forms.Form):

    tarea = forms.IntegerField()
    producto = forms.IntegerField()
    cantidad = forms.IntegerField()

class ObservacionForm(forms.Form):
    tarea = forms.IntegerField()
    contenido = forms.CharField()

class AceptarTareaForm(forms.Form):
    orden_id = forms.IntegerField()
    tareas = forms.MultipleChoiceField()

class CrearTareaForm(forms.Form):
    orden_id = forms.IntegerField()
    tipo_tarea = forms.IntegerField()
    observacion = forms.CharField()
