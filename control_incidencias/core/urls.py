
from django.urls import path

from .views import index, inicio_sesion, logout, logout_view, login_view, register, reset_password
from .views import dashboard_admin
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
    
    #CLIENTE
    path('dashboard-cliente', dashboard_cliente, name="dashboard_cliente"),
    
    path('accounts/*', inicio_sesion, name="accounts_login"),
]
