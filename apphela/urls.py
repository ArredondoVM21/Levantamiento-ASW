from django.urls import path
from . import views

urlpatterns = [
    path('', views.bienvenida, name='principal'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Ítems
    path('items/', views.lista_items, name='lista_items'),
    path('items/crear/', views.crear_item, name='crear_item'),
    path('items/<int:pk>/', views.detalle_item, name='detalle_item'),
    path('items/<int:pk>/editar/', views.editar_item, name='editar_item'),
    path('items/<int:pk>/eliminar/', views.eliminar_item, name='eliminar_item'),

    # Presupuestos
    path('presupuestos/', views.lista_presupuestos, name='lista_presupuestos'),
    path('presupuestos/crear/', views.crear_presupuesto, name='crear_presupuesto'),
    path('presupuestos/<int:pk>/', views.detalle_presupuesto, name='detalle_presupuesto'),
    path('presupuestos/<int:pk>/editar/', views.editar_presupuesto, name='editar_presupuesto'),
    path('presupuestos/<int:pk>/copiar/', views.copiar_presupuesto, name='copiar_presupuesto'),
    path('presupuestos/<int:pk>/eliminar/', views.eliminar_presupuesto, name='eliminar_presupuesto'),
]
