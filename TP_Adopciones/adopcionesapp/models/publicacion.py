"""
Modelo Publicacion para gestionar las publicaciones de animales en adopción.
"""

from django.db import models
from django.contrib.auth.models import User
from .animal import Animal

class Publicacion(models.Model):
    """
    Modelo que representa una publicación de un animal en adopción.
    """
    ESTADOS = [
        ("REV", "Revisión"),
        ("APR", "Aprobada"),
        ("SUS", "Suspendida"),
    ]
    titulo = models.CharField(max_length=100, blank=False, null=False)
    estado = models.CharField(max_length=3, choices=ESTADOS, default="REV")
    animal = models.OneToOneField(Animal, on_delete=models.CASCADE, related_name="publicacion")
    hogar_actual = models.CharField(max_length=100, blank=False, null=False)
    condiciones_adopcion = models.TextField(blank=False, null=False)
    historia = models.TextField(blank=True, null=True)
    recomendaciones_cuidado = models.TextField(blank=True, null=True)
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="publicaciones")
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    adoptado = models.BooleanField(default=False)

    def __str__(self):
        return f"Publicación de {self.animal.nombre} ({self.animal.tipo_animal})"
