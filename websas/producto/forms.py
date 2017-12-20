from django import forms
from .models import Producto, ReservaStock

class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = [
            'nombre',
            'descripcion',
            'marca',
            'stock_minimo',
            'stock',
            'precio',
        ]
        labels = {
            'nombre':'Nombre',
            'descripcion':'Descripcion',
            'marca':'Marca',
            'stock_minimo':'Stock minimo',
            'stock':'Stock actual',
            'precio':'Precio $',
        }
        error_messages = {
            'nombre' : {
                'max_length' : ("Nombre demasiado largo. No debe exceder los 20 caracteres."),
            },
            'descripcion' : {
                'max_length' : ("Descripcion demasiado larga. No debe exceder los 50 caracteres."),
            },
            'marca' : {
                'max_length' : ("Nombre de marca demasiado largo. No debe exceder los 20 caracteres."),
            }
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'descripcion': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'marca': forms.TextInput(attrs={'class':'form-control col-md-7 col-xs-12'}),
            'stock_minimo': forms.NumberInput(attrs={
                'class':'form-control col-md-7 col-xs-12',
                'data-validate-minmax': '0,',
                }),
            'stock': forms.NumberInput(attrs={
                'class':'form-control col-md-7 col-xs-12',
                'data-validate-minmax': '0,',
                }),
            'precio': forms.NumberInput(attrs={
                'class':'form-control col-md-7 col-xs-12',
                'data-validate-minmax': '0,',
                }),
        }

class ProductoUpdateForm(ProductoForm):

    stock_disponible = forms.NumberInput()
    stock_reservado = forms.NumberInput()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stock_disponible = kwargs.get('instance').stock_disponible
        self.stock_reservado = kwargs.get('instance').stock_reservado
         
    class Meta(ProductoForm.Meta):
        # fields = ProductoForm.Meta.fields + ('stock_disponible', 'stock_reservado')
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class':'form-control col-md-7 col-xs-12',
                'readonly':'True',
                }),
            'descripcion': forms.TextInput(attrs={
                'class':'form-control col-md-7 col-xs-12'
                }),
            'marca': forms.TextInput(attrs={
                'class':'form-control col-md-7 col-xs-12'
                }),
            'stock_minimo': forms.NumberInput(attrs={
                'class':'form-control col-md-7 col-xs-12'
                }),
            'stock': forms.NumberInput(attrs={
                'class':'form-control col-md-7 col-xs-12',
                }),
            'stock_disponible': forms.NumberInput(attrs={
                'class':'form-control col-md-7 col-xs-12',
                'name':'stock_disponible',
                'readonly':'True',
                }),
            'stock_reservado': forms.NumberInput(attrs={
                'class':'form-control col-md-7 col-xs-12',
                'name':'stock_reservado',
                'readonly':'True',
                }),
            'precio': forms.NumberInput(attrs={
                'class':'form-control col-md-7 col-xs-12'
                }),
        }


class ReservaCancelarForm(forms.Form):
    reserva_id = forms.IntegerField()

    def clean(self):
        if not ReservaStock.objects.filter(pk=self.cleaned_data.get("reserva_id")).exists():
            raise forms.ValidationError("No existe la reserva")

    def save(self, commit=True):
        reserva = ReservaStock.objects.get(pk=self.cleaned_data.get("reserva_id"))
        reserva.cancelar()

class ReservaModificarForm(forms.Form):
    reserva_id = forms.IntegerField()
    cantidad = forms.IntegerField()

    def clean(self):
        if not ReservaStock.objects.filter(pk=self.cleaned_data.get("reserva_id")).exists():
            raise forms.ValidationError("No existe la reserva")

    def save(self, commit=True):
        
        reserva = ReservaStock.objects.get(pk=self.cleaned_data.get("reserva_id"))
        reserva.cantidad = self.cleaned_data.get("cantidad")
        reserva.save()
