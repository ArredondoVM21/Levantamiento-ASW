from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.core.validators import RegexValidator, MaxLengthValidator


class Reporte(models.Model):
    TIPO_CHOICES = (
        ('PDF', 'PDF'),
        ('EXCEL', 'Excel'),
    )

    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    archivo = models.FileField(upload_to='reportes/')
    fecha = models.DateTimeField(auto_now_add=True)
    generado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.nombre} - {self.tipo}"


class CuentaPorPagar(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('vencido', 'Vencido'),
    ]

    numero_boleta = models.CharField(
        max_length=15,
        unique=True,
        validators=[
            RegexValidator(
                r'^[A-Za-z0-9\-]+$',
                'Solo se permiten letras, números y guiones.'
            )
        ]
    )

    descripcion = models.TextField(
        blank=True,
        null=True,
        validators=[MaxLengthValidator(250)]
    )

    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()

    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente'
    )

    fecha_registro = models.DateTimeField(auto_now_add=True)
    generado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    @property
    def dias_restantes(self):
        return (self.fecha_vencimiento - date.today()).days

    # actualiza el estado segun las fechas
    def actualizar_estado(self):
        if self.estado == 'pagado':
            return self.estado

        if self.fecha_vencimiento < date.today():
            self.estado = 'vencido'
        else:
            self.estado = 'pendiente'

        return self.estado


    def __str__(self):
        return f"Boleta {self.numero_boleta}"
