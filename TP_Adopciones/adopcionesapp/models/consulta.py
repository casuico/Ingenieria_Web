"""
Modelo Consulta para almacenar las consultas realizadas sobre publicaciones.
"""

from django.db import models
from django.contrib.auth.models import User
from .publicacion import Publicacion

class Consulta(models.Model):
    """
    Modelo que almacena las consultas de los usuarios sobre una publicación.
    """
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    asunto = models.CharField(max_length=100, default="")
    mensaje = models.TextField(max_length=1000)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.asunto
