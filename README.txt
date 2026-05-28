Sistema de Control de Finanzas - Presupuestos

Sistema web desarrollado en Django para la gestión de presupuestos, categorías y movimientos financieros de Secreto Helado,
 una heladería artesanal.
El proyecto permite llevar control sobre ingresos, gastos, presupuestos mensuales y categorías asociadas.


Características principales

* Autenticación de usuarios (login/logout con Django Auth).
* CRUD completo de **categorías**, **presupuestos** y **transferencias**.
* Validaciones y mensajes de éxito/error.
* Interfaz moderna con **Bootstrap 5** y **Crispy Forms**.
* Base de datos **MySQL** (configurada en `settings.py`).
* Paginación.


Migraciones y ejecución

Crear migraciones

> python manage.py makemigrations
> python manage.py migrate


Crear usuario administrador

> python manage.py createsuperuser


Ejecutar servidor

> python manage.py runserver

Abre tu navegador y visita:

http://127.0.0.1:8000


Credenciales de usuarios

Usuario 1:

* Usuario: Admin
* Contraseña: Admin012

Usuario 2:

* Usuario: administrado
* Correo: Admin@gmail.com
* Contraseña: admin0


Desarrollado con:

>Python 3.11+
>Django 5.2
>Bootstrap 5 / Crispy Forms
>MySQL


Autores:

Proyecto académico desarrollado por:
Valker Arredondo y Nicolás Zepeda
Estudiantes de Ingeniería en Informática.


Nota:
> Este sistema está configurado para ejecutarse únicamente en entorno local (localhost), es lo mismo que el de AWS solo que localhost.
