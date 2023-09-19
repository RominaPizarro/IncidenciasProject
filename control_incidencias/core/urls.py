
from django.urls import path

from .views import index, inicio_sesion, logout, logout_view, login_view, register, reset_password
from .views import dashboard_admin
from .views import usuario_index, usuario_create, usuario_update, usuario_delete
from .views import area_index, area_create, area_update, area_delete

from .views import dashboard_cliente

urlpatterns = [
    path('', index, name="index"),
    path('login', inicio_sesion, name="login"),    
    path('logout', logout_view, name="logout"),
    
    
    path('login_view', login_view, name="login_view"),
    path('register', register, name="register"),
    path('reset-password', reset_password, name="reset_password"),
    
    #ADMIN
    path('dashboard-admin', dashboard_admin, name="dashboard_admin"),
    
    path('usuarios', usuario_index, name="usuario_index"),
    path('usuarios/create', usuario_create, name="usuario_create"),
    path('usuarios/<int:id>', usuario_update, name="usuario_update"),
    path('usuarios/<int:id>/delete', usuario_delete, name="usuario_delete"),
    
    path('areas', area_index, name="area_index"),
    path('areas/create', area_create, name="area_create"),
    path('areas/<int:id>', area_update, name="area_update"),
    path('areas/<int:id>/delete', area_delete, name="area_delete"),
    
    #CLIENTE
    path('dashboard-cliente', dashboard_cliente, name="dashboard_cliente"),
    
    path('accounts/*', inicio_sesion, name="accounts_login"),
]
