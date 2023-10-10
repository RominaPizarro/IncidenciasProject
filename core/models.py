from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

# Create your models here.

class Area(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Estado(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    rut = models.CharField(max_length=100, unique=True)
    telefono = models.CharField(max_length=100, null=True, blank=True)
    fecha_nacimiento = models.DateField()
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=settings.ROLES)
    
    def __str__(self):
        return self.rut + ' - ' + self.user.first_name + ' ' + self.user.last_name

class Requerimiento(models.Model):
    codigo = models.CharField(max_length=100, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=500)
    observaciones = models.CharField(max_length=1000, null=True, blank=True)
    usuario_reporta = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='requerimientos_reporta')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='requerimientos')
    usuario_asignado = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='requerimientos_asignado', null=True)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='requerimientos')

