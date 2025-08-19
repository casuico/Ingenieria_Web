from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField
from django.core.exceptions import ValidationError
import os
from cloudinary.models import CloudinaryField
from cloudinary.models import CloudinaryResource
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile


class Publicacion(models.Model):
    TIPO_ANIMAL_CHOICES = [
        ('Perro', 'Perro'),
        ('Gato', 'Gato'),
        ('Conejo', 'Conejo'),
        ('Otro', 'Otro'),
    ]
    SEXO_CHOICES = [
        ('M', 'Macho'),
        ('H', 'Hembra'),
    ]

    nombre = models.CharField(max_length=50, blank=False, null=False)
    tipo_animal = models.CharField(max_length=10, choices=TIPO_ANIMAL_CHOICES)
    raza = models.CharField(max_length=50, blank=True, null=False)
    edad = models.PositiveIntegerField(help_text="Edad en años")
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)

    # Salud
    castrado = models.BooleanField(default=False)
    enfermedades = models.TextField(blank=True, null=True)
    
    # Vacunas como lista
    vacunas = JSONField(default=list, blank=True)  # Lista de strings

    # Comportamiento y compatibilidad
    compatibilidad_otros_animales = models.BooleanField(default=True)
    compatibilidad_ninos = models.BooleanField(default=True)
    comportamiento = models.TextField(blank=True, null=True)

    # Ubicación y logística
    hogar_actual = models.CharField(max_length=100, blank=False, null=False)
    condiciones_adopcion = models.TextField(blank=False, null=False)

    # Información adicional
    historia = models.TextField(blank=True, null=True)
    recomendaciones_cuidado = models.TextField(blank=True, null=True)
    contacto = models.CharField(max_length=100)

    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name="publicaciones")

    # Timestamps
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.tipo_animal})"


class Consulta(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    asunto = models.CharField(max_length=100, default="")
    mensaje = models.TextField(max_length=1000)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.asunto


class Multimedia(models.Model):
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
    archivo = CloudinaryField(resource_type="auto")

    def __str__(self):
        return f"{self.tipo} de {self.publicacion.nombre}"
    

    def clean(self):
        super().clean()

        if not self.archivo:
            return

        if isinstance(self.archivo, CloudinaryResource):
            ext = self.archivo.format.lower()
        elif isinstance(self.archivo, (InMemoryUploadedFile, TemporaryUploadedFile)):
            ext = os.path.splitext(self.archivo.name)[1].lower().lstrip(".")  # quitar el punto
        else:
            raise ValidationError("No se pudo determinar el tipo de archivo.")

        # Validación por tipo
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
