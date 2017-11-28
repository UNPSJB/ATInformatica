from django import forms
from .models import Tarifa

class TarifaUpdateForm(forms.Form):

    tarifa_id = forms.IntegerField()
    precio = forms.DecimalField()
    
    def clean(self):
        cleaned_data = super(self.__class__, self).clean()
        id_tarifa = cleaned_data.get("tarifa_id")
        if not Tarifa.objects.filter(id=id_tarifa).exists():
            raise forms.ValidationError(
                "La tarifa no existe"
            )

    def save(self, commit=True):
        tarifa = Tarifa.objects.get(id=self.cleaned_data.get("tarifa_id"))
        tarifa.actualizar_precio(self.cleaned_data.get("precio"))

    