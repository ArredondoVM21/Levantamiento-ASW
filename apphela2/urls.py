from django.urls import path
from . import views

urlpatterns = [
    path("informes/", views.informes, name="informes"),
    path("informes/generar/<int:id>/pdf/", views.generar_pdf, name="generar_pdf"),
    path("informes/generar/<int:id>/excel/", views.generar_excel, name="generar_excel"),
    
    # Cuentas por pagar
    path("cuentas/", views.lista_cuentas, name="lista_cuentas"),
    path("cuentas/crear/", views.crear_cuenta, name="crear_cuenta"),
    path("cuentas/<int:pk>/", views.detalle_cuenta, name="detalle_cuenta"),
    path("cuentas/<int:pk>/editar/", views.editar_cuenta, name="editar_cuenta"),
    path("cuentas/<int:pk>/eliminar/", views.eliminar_cuenta, name="eliminar_cuenta"),
]
