from django.db import models
from cloudinary.models import CloudinaryField, CloudinaryResource
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
import os
from .publicacion import Publicacion

class Multimedia(models.Model):
    # ...existing code...
    TIPO_CHOICES = [
        ('imagen', 'Imagen'),
        ('video', 'Video'),
    ]
    publicacion = models.ForeignKey(
        Publicacion,
        on_delete=models.CASCADE,
        related_name="multimedia"
    )
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    archivo = CloudinaryField(resource_type="auto", blank=False, null=False)

    def __str__(self):
        return f"{self.tipo} de {self.publicacion.titulo}"

    def clean(self):
        # ...existing code...
        super().clean()
        if not self.archivo:
            return
        if isinstance(self.archivo, CloudinaryResource):
            ext = self.archivo.format.lower()
        elif isinstance(self.archivo, (InMemoryUploadedFile, TemporaryUploadedFile)):
            ext = os.path.splitext(self.archivo.name)[1].lower().lstrip(".")
        else:
            raise ValidationError("No se pudo determinar el tipo de archivo.")
        if self.tipo == "imagen":
            if ext not in ['jpg', 'jpeg', 'png', 'gif']:
                raise ValidationError(
                    "Extensión de archivo incorrecta, solo se permiten '.jpg', '.jpeg', '.png', '.gif'."
                )
        elif self.tipo == "video":
            if ext not in ['mp4', 'mov', 'avi', 'mkv', 'webm']:
                raise ValidationError(
                    "Extensión de archivo incorrecta, solo se permiten '.mp4', '.mov', '.avi', '.mkv', '.webm'."
                )

