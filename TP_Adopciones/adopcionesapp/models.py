# adopciones/models.py
from django.db import models

class Publicacion(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    tipo_animal = models.CharField(max_length=50)
    edad = models.IntegerField()

    def __str__(self):
        return self.titulo