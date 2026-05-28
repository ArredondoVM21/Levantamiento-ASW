from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from datetime import date
from django.db.models import PROTECT

class ItemPresupuesto(models.Model):
    id_item = models.AutoField(primary_key=True)
    nombre = models.CharField(
        max_length=50,
        verbose_name='Nombre del Ítem'
    )

    descripcion = models.TextField(
        verbose_name='Descripción del Ítem',
        blank=True,
        null=True,
        max_length=200
    )

    class Meta:
        verbose_name = 'ítem de presupuesto'
        verbose_name_plural = 'ítems de presupuesto'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre}"


class Presupuesto(models.Model):
    MESES = [
        ('Enero', 'Enero'),
        ('Febrero', 'Febrero'),
        ('Marzo', 'Marzo'),
        ('Abril', 'Abril'),
        ('Mayo', 'Mayo'),
        ('Junio', 'Junio'),
        ('Julio', 'Julio'),
        ('Agosto', 'Agosto'),
        ('Septiembre', 'Septiembre'),
        ('Octubre', 'Octubre'),
        ('Noviembre', 'Noviembre'),
        ('Diciembre', 'Diciembre'),
    ]

    fecha = models.DateField(verbose_name='Fecha de realización o modificación')
    mes = models.CharField(max_length=20, choices=MESES, verbose_name='Mes')
    anio = models.PositiveIntegerField(
        verbose_name='Año',
        validators=[MaxValueValidator(9999)]
    )
    descripcion = models.TextField(verbose_name='Descripción general')

    class Meta:
        verbose_name = 'Presupuesto'
        verbose_name_plural = 'Presupuestos'
        ordering = ['-anio', '-mes']
        # evitar presupuestos duplicados por mes y año
        constraints = [
            models.UniqueConstraint(fields=['mes', 'anio'], name='unique_mes_anio')
        ]

    def __str__(self):
        return f"{self.mes} {self.anio}"

class DetallePresupuesto(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE, related_name='detalles')
    item = models.ForeignKey(ItemPresupuesto, on_delete=PROTECT, verbose_name='Ítem')
    monto_limite = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Límite asignado')

    def __str__(self):
        return f"{self.item.nombre} - {self.presupuesto}"