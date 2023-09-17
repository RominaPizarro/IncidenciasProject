from django.contrib import admin

from control_incidencias.core.models import *

# Register your models here.

admin.site.register(Area)
admin.site.register(Rol)
admin.site.register(Estado)
admin.site.register(Usuario)
admin.site.register(Requerimiento)