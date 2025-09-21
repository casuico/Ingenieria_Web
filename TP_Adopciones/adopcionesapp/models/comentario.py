from django.db import models
from django.contrib.auth.models import User
from .publicacion import Publicacion

class Comentario(models.Model):
    # ...existing code...
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("aprobado", "Aprobado"),
        ("rechazado", "Rechazado"),
    ]
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name="comentarios")
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField(max_length=500, blank=False, null=False)
    creado = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADOS, default="pendiente")

    def __str__(self):
        return f"Comentario de {self.autor} en {self.publicacion}"

