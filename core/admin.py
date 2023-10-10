from django.contrib import admin

from .models import Area, Estado, Usuario, Requerimiento

# Register your models here.

admin.site.register(Area)
admin.site.register(Estado)
admin.site.register(Usuario)
admin.site.register(Requerimiento)