from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Presupuesto, DetallePresupuesto, ItemPresupuesto
from .forms import PresupuestoForm, DetallePresupuestoFormSet, ItemPresupuestoForm

def bienvenida(request):
    return redirect('dashboard')

@login_required
def dashboard(request):
    presupuestos = Presupuesto.objects.all().order_by('-fecha')[:5]
    items = ItemPresupuesto.objects.all().order_by('nombre')[:5]
    return render(request, 'dashboard.html', {'presupuestos': presupuestos, 'items': items})

# ÍTEMS
@login_required
def lista_items(request):
    items = ItemPresupuesto.objects.all().order_by('nombre')
    paginator = Paginator(items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'items/lista_items.html', {'items': page_obj})

@login_required
def crear_item(request):
    if request.method == 'POST':
        form = ItemPresupuestoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Ítem creado exitosamente.")
            return redirect('lista_items')
    else:
        form = ItemPresupuestoForm()
    return render(request, 'items/crear_item.html', {'form': form})

@login_required
def editar_item(request, pk):
    item = get_object_or_404(ItemPresupuesto, pk=pk)
    if request.method == 'POST':
        form = ItemPresupuestoForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Ítem actualizado correctamente.")
            return redirect('lista_items')
    else:
        form = ItemPresupuestoForm(instance=item)
    return render(request, 'items/editar_item.html', {'form': form, 'item': item})

@login_required
def eliminar_item(request, pk):
    item = get_object_or_404(ItemPresupuesto, pk=pk)
    asociado = DetallePresupuesto.objects.filter(item=item).exists()

    if request.method == 'POST':
        if asociado:
            messages.error(request, "No se puede eliminar este ítem porque está asociado a uno o más presupuestos.")
            return redirect('lista_items')
        try:
            item.delete()
            messages.success(request, "Ítem eliminado correctamente.")
        except Exception as e:
            messages.error(request, f"Error al eliminar el ítem: {e}")
        return redirect('lista_items')

    return render(request, 'items/eliminar_item.html', {'item': item, 'asociado': asociado})

@login_required
def detalle_item(request, pk):
    item = get_object_or_404(ItemPresupuesto, pk=pk)
    asociado = DetallePresupuesto.objects.filter(item=item).exists()
    return render(request, 'items/detalle_item.html', {
        'item': item,
        'asociado': asociado
    })

# LISTAR PRESUPUESTOS
@login_required
def lista_presupuestos(request):
    presupuestos = Presupuesto.objects.all().order_by('-anio', '-mes')
    for presupuesto in presupuestos:
        presupuesto.monto_total_asignado = sum(
            detalle.monto_limite for detalle in presupuesto.detalles.all()
        )
    return render(request, 'presupuestos/lista_presupuestos.html', {'presupuestos': presupuestos})

# CREAR PRESUPUESTO
@login_required
def crear_presupuesto(request):
    if request.method == 'POST':
        form = PresupuestoForm(request.POST)
        formset = DetallePresupuestoFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            presupuesto = form.save()
            detalles = formset.save(commit=False)
            for detalle in detalles:
                detalle.presupuesto = presupuesto
                detalle.save()

            messages.success(request, f"Presupuesto '{presupuesto.mes} {presupuesto.anio}' creado exitosamente.")
            
            # limpia el formulario y permanecemos en la página
            form = PresupuestoForm()
            formset = DetallePresupuestoFormSet()
        else:
            # Eliminamos el mensaje general de error para que solo se muestren los errores específicos
            print("Errores del form:", form.errors)
            print("Errores del formset:", formset.errors)
    else:
        form = PresupuestoForm()
        formset = DetallePresupuestoFormSet()

    return render(request, 'presupuestos/crear_presupuesto.html', {
        'form': form,
        'formset': formset
    })

# EDITAR PRESUPUESTO
@login_required
def editar_presupuesto(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)
    form = PresupuestoForm(request.POST or None, instance=presupuesto)
    formset = DetallePresupuestoFormSet(request.POST or None, instance=presupuesto)

    if request.method == 'POST':
        if form.is_valid() and formset.is_valid():
            presupuesto = form.save()

            # Guardamos pero sin confirmar aún (para poder borrar)
            detalles = formset.save(commit=False)

            # 1) Guardar los detalles nuevos o editados
            for detalle in detalles:
                detalle.presupuesto = presupuesto
                detalle.save()

            # 2) Borrar los marcados para eliminar
            for detalle_form in formset.deleted_forms:
                if detalle_form.instance.pk:
                    detalle_form.instance.delete()

            messages.success(request, "Presupuesto actualizado correctamente.")
            return redirect('lista_presupuestos')
        else:
            print("Errores form principal:", form.errors)
            for i, sub in enumerate(formset):
                print(f"Formset {i} errors:", sub.errors)
            print("Errores globales formset:", formset.non_form_errors())

    return render(request, 'presupuestos/editar_presupuesto.html', {
        'form': form,
        'formset': formset,
        'presupuesto': presupuesto
    })


# COPIA DE PRESUPUESTO
@login_required
def copiar_presupuesto(request, pk):
    presupuesto_original = get_object_or_404(Presupuesto, pk=pk)

    nuevo_mes = presupuesto_original.mes
    nuevo_anio = presupuesto_original.anio

    # Buscar el primer año disponible que no esté ocupado por este mes
    while Presupuesto.objects.filter(mes=nuevo_mes, anio=nuevo_anio).exists():
        nuevo_anio += 1  # Avanzamos al siguiente año

    # Crear descripción indicando copia
    descripcion_copia = f"{presupuesto_original.descripcion} (Copia)"

    # Crear presupuesto nuevo
    presupuesto_copia = Presupuesto.objects.create(
        fecha=timezone.now().date(),
        mes=nuevo_mes,
        anio=nuevo_anio,
        descripcion=descripcion_copia
    )

    # Copiar los detalles asociados
    detalles_originales = DetallePresupuesto.objects.filter(presupuesto=presupuesto_original)
    for detalle in detalles_originales:
        DetallePresupuesto.objects.create(
            presupuesto=presupuesto_copia,
            item=detalle.item,
            monto_limite=detalle.monto_limite
        )

    messages.success(request, f"Copia del presupuesto '{presupuesto_original}' creada correctamente.")
    return redirect('lista_presupuestos')


# DETALLE PRESUPUESTO
@login_required
def detalle_presupuesto(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)
    detalles = DetallePresupuesto.objects.filter(presupuesto=presupuesto)

    # Calcular el monto total asignado
    monto_total_asignado = sum(detalle.monto_limite for detalle in detalles)

    return render(request, 'presupuestos/detalle_presupuesto.html', {
        'presupuesto': presupuesto,
        'detalles': detalles,
        'monto_total_asignado': monto_total_asignado,
    })

# ELIMINAR PRESUPUESTO
@login_required
def eliminar_presupuesto(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)
    if request.method == 'POST':
        presupuesto.delete()
        messages.success(request, "Presupuesto eliminado correctamente.")
        return redirect('lista_presupuestos')
    return render(request, 'presupuestos/eliminar_presupuesto.html', {'presupuesto': presupuesto})