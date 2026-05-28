from django import forms
from .models import CuentaPorPagar

class CuentaPorPagarForm(forms.ModelForm):
    class Meta:
        model = CuentaPorPagar
        fields = [
            'numero_boleta',
            'descripcion',
            'fecha_emision',
            'fecha_vencimiento',
            'monto',
            'estado'
        ]

        widgets = {
            'numero_boleta': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '15',
                'placeholder': 'Ej: BO-1234 o A001',
                'oninput': "this.value = this.value.replace(/[^A-Za-z0-9\\-]/g, '')"
            }),

            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'maxlength': '250',
                'rows': 3,
                'placeholder': 'Máximo 250 caracteres...',
                'oninput': "if(this.value.length > 250) this.value = this.value.slice(0,250);"
            }),

            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '9999999.99',
                'oninput': """
                    if(this.value.length > 12) 
                        this.value = this.value.slice(0,12);
                """
            }),

            'fecha_emision': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'fecha_vencimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'estado': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

