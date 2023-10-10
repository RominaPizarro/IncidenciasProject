
from django.urls import path

from .views import index, inicio_sesion, mi_api, logout, logout_view, login_view, register, reset_password, change_password
from .views import dashboard_admin
from .views import usuario_index, usuario_create, usuario_update, usuario_delete, usuario_perfil_admin, usuario_perfil
from .views import area_index, area_create, area_update, area_delete
from .views import estado_index, estado_create, estado_update, estado_delete
from .views import requerimiento_index, requerimiento_create, requerimiento_update, requerimiento_delete, requerimiento_asignar, requerimiento_atender, mis_requerimientos, requerimiento_nuevo

from .views import dashboard_cliente

from .views import RequerimientoApiView, MyTokenObtainPairView, MyTokenRefreshView

urlpatterns = [
    path('', index, name="index"),
    path('login', inicio_sesion, name="login"),    
    path('logout', logout_view, name="logout"),
    
    
    path('login_view', login_view, name="login_view"),
    path('register', register, name="register"),
    path('reset-password', reset_password, name="reset_password"),
    path('change-password/<int:user_id>', change_password, name="change_password"),
    
    #ADMIN
    path('dashboard-admin', dashboard_admin, name="dashboard_admin"),
    
    path('usuarios', usuario_index, name="usuario_index"),
    path('usuarios/create', usuario_create, name="usuario_create"),
    path('usuarios/<int:id>', usuario_update, name="usuario_update"),
    path('usuarios/<int:id>/delete', usuario_delete, name="usuario_delete"),
    path('usuario-admin/perfil', usuario_perfil_admin, name="usuario_perfil_admin"),
    path('usuario/perfil', usuario_perfil, name="usuario_perfil"),
    
    path('areas', area_index, name="area_index"),
    path('areas/create', area_create, name="area_create"),
    path('areas/<int:id>', area_update, name="area_update"),
    path('areas/<int:id>/delete', area_delete, name="area_delete"),
    
    path('estados', estado_index, name="estado_index"),
    path('estados/create', estado_create, name="estado_create"),
    path('estados/<int:id>', estado_update, name="estado_update"),
    path('estados/<int:id>/delete', estado_delete, name="estado_delete"),
    
    path('requerimientos', requerimiento_index, name="requerimiento_index"),
    path('requerimientos/create', requerimiento_create, name="requerimiento_create"),
    path('requerimientos/<int:id>', requerimiento_update, name="requerimiento_update"),
    path('requerimientos/<int:id>/asignar', requerimiento_asignar, name="requerimiento_asignar"),
    path('requerimientos/<int:id>/delete', requerimiento_delete, name="requerimiento_delete"),
    
    #CLIENTE
    path('dashboard-cliente', dashboard_cliente, name="dashboard_cliente"),
    path('requerimientos/<int:id>/atender', requerimiento_atender, name="requerimiento_atender"),
    path('requerimientos/nuevo', requerimiento_nuevo, name="requerimiento_nuevo"),
    path('mis_requerimientos', mis_requerimientos, name="mis_requerimientos"),
    
    path('accounts/*', inicio_sesion, name="accounts_login"),
    
    # API REST
    path('api', mi_api, name='api'),
    path('api/requerimientos', RequerimientoApiView.as_view(), name='requerimientos'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),

]
