from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Rutas de apphela (la que tiene principal y dashboard)
    path('', include('apphela.urls')),

    # Rutas de apphela2 (reportes, cuentas, etc.)
    path('finanzas/', include('apphela2.urls')),

    # Login y logout
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html'), 
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
