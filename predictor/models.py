from django.db import models
from django.contrib.auth.models import User

class HistorialPrediccion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    satisfaccion = models.FloatField()
    antiguedad = models.IntegerField()
    salario = models.CharField(max_length=50)
    departamento = models.CharField(max_length=100)
    resultado = models.BooleanField()

    def __str__(self):
        return f'{self.usuario.username} - {self.resultado} ({self.fecha})'
