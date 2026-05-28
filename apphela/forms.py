from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from datetime import date
from .models import Presupuesto, ItemPresupuesto, DetallePresupuesto

class ItemPresupuestoForm(forms.ModelForm):
    class Meta:
        model = ItemPresupuesto
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '50'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'maxlength': '200'
            }),
        }


class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['fecha', 'mes', 'anio', 'descripcion']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'mes': forms.Select(attrs={'class': 'form-select'}),
            'anio': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': date.today().year,
                'max': 9999,
                'maxlength': 4,
                'oninput': 'this.value=this.value.slice(0,4)'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'maxlength': 500 
            }),
        }


    # Validar que la fecha no sea anterior al día actual
    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        hoy = date.today()
        if fecha and fecha < hoy:
            raise ValidationError("La fecha no puede ser anterior al día actual.")
        return fecha

    # Validar que el año no sea menor al año actual ni mayor a 9999
    def clean_anio(self):
        anio = self.cleaned_data.get('anio')
        anio_actual = date.today().year

        if anio and anio < anio_actual:
            raise ValidationError(f"El año no puede ser menor al actual ({anio_actual}).")

        if anio and anio > 9999:
            raise ValidationError("El año no puede tener más de 4 dígitos.")

        if anio and len(str(anio)) != 4:
            raise ValidationError("El año debe tener exactamente 4 dígitos.")

        return anio


    # Nueva validación para evitar presupuestos duplicados por mes y año
    def clean(self):
        cleaned_data = super().clean()
        mes = cleaned_data.get('mes')
        anio = cleaned_data.get('anio')

        # Verificar si ya existe un presupuesto con ese mes y año
        if mes and anio:
            existe = Presupuesto.objects.filter(mes=mes, anio=anio).exclude(pk=self.instance.pk).exists()
            if existe:
                raise ValidationError("Ya existe un presupuesto para ese mes y año.")

        return cleaned_data

class DetallePresupuestoForm(forms.ModelForm):
    class Meta:
        model = DetallePresupuesto
        fields = ['item', 'monto_limite']
        widgets = {
            'item': forms.Select(attrs={'class': 'form-select'}),
            'monto_limite': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1000',
                'step': '1'
            }),
        }

    # Redondear valor al mostrarlo en el campo
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.monto_limite is not None:
            self.initial['monto_limite'] = int(round(self.instance.monto_limite))

    # Validar que el monto no sea menor a 1000
    def clean_monto_limite(self):
        monto = self.cleaned_data.get('monto_limite')
        if monto is None:
            raise ValidationError("Debe ingresar un monto.")
        if monto < 1000:
            raise ValidationError("El monto mínimo permitido es 1000.")
        return monto

# Formset vinculado entre Presupuesto y sus detalles
DetallePresupuestoFormSet = inlineformset_factory(
    Presupuesto,
    DetallePresupuesto,
    form=DetallePresupuestoForm,
    extra=1,
    can_delete=True
)