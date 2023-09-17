from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

# Create your models here.

class Area(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.id) + '. ' + self.nombre

class Rol(models.Model):
    descripcion = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return str(self.id) + '. ' + self.descripcion

class Estado(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    descripcion = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.id) + '. ' + self.nombre

class Usuario(models.Model):
    rut = models.CharField(max_length=100, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)    
    email = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100, null=True, blank=True)
    fecha_nacimiento = models.DateField()
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, related_name='usuarios')

    def __str__(self):
        return str(self.id) + '. ' + self.rut + ' - ' + self.nombres + ' ' + self.apellidos

class Requerimiento(models.Model):
    codigo = models.CharField(max_length=100, unique=True)
    fecha_registro = models.DateTimeField()
    descripcion = models.CharField(max_length=500)
    usuario_reporta = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='requerimientos_reporta')
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='requerimientos')
    usuario_asignado = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='requerimientos_asignado')
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='requerimientos')