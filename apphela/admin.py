from django.contrib import admin
from .models import Presupuesto, DetallePresupuesto

class DetallePresupuestoInline(admin.TabularInline):
    model = DetallePresupuesto
    extra = 1
    fields = ('item', 'monto_limite')
    verbose_name = "Ítem del Presupuesto"
    verbose_name_plural = "Ítems del Presupuesto"


@admin.register(Presupuesto)
class PresupuestoAdmin(admin.ModelAdmin):
    list_display = ('mes', 'anio', 'fecha', 'descripcion')
    search_fields = ('mes', 'anio', 'descripcion')
    list_filter = ('mes', 'anio')
    ordering = ('-anio', '-fecha')
    inlines = [DetallePresupuestoInline]
    fieldsets = (
        ('Información del Presupuesto', {
            'fields': ('fecha', 'mes', 'anio', 'descripcion')
        }),
    )


@admin.register(DetallePresupuesto)
class DetallePresupuestoAdmin(admin.ModelAdmin):
    list_display = ('item', 'monto_limite', 'presupuesto')
    search_fields = ('item', 'presupuesto__descripcion')
    list_filter = ('presupuesto__mes', 'presupuesto__anio')
    ordering = ('presupuesto__anio', 'presupuesto__mes')
