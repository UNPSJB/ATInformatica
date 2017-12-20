from django import forms
from .models import TipoTarea
from producto.models import ReservaStock, Producto
from tarea.models import TipoTarea, Tarea

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

    def clean(self):

        if not Tarea.objects.filter(pk=self.cleaned_data['tarea']).exists():
            raise forms.ValidationError("No existe la tarea")
        
        if not Producto.objects.filter(pk=self.cleaned_data['producto']).exists():
            raise forms.ValidationError("No existe el producto")

        if self.cleaned_data['cantidad'] <= 0:
            raise forms.ValidationError("La cantidad es inválida")
        
    def save(self, commit=True):

        tarea = Tarea.objects.get(pk=self.cleaned_data['tarea'])
        producto = Producto.objects.get(pk=self.cleaned_data['producto'])
        cantidad = self.cleaned_data['cantidad']
        
        tarea.hacer("reservar_stock", producto=producto, cantidad=cantidad)

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
