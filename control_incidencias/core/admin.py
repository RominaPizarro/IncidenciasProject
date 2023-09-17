from django.contrib import admin

from .models import Area, Rol, Estado, Usuario, Requerimiento

# Register your models here.

admin.site.register(Area)
admin.site.register(Rol)
admin.site.register(Estado)
admin.site.register(Usuario)
admin.site.register(Requerimiento)