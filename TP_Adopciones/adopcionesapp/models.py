from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField
from django.core.exceptions import ValidationError
import os
from cloudinary.models import CloudinaryField
from cloudinary.models import CloudinaryResource
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.dispatch import receiver
from django.db.models.signals import post_save


class Animal(models.Model):
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
    tipo_animal = models.CharField(max_length=10, choices=TIPO_ANIMAL_CHOICES, blank=False, null=False)
    raza = models.CharField(max_length=50, blank=False, null=False)
    edad = models.PositiveIntegerField(help_text="Edad en años", blank=False, null=False)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=False, null=False)

    castrado = models.BooleanField(default=False, blank=False, null=False)
    enfermedades = models.TextField(blank=True, null=True)
    vacunas = models.TextField(blank=True, null=True)

    compatibilidad_otros_animales = models.BooleanField(default=True)
    compatibilidad_ninos = models.BooleanField(default=True)
    comportamiento = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.tipo_animal})"


class Publicacion(models.Model):
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
    archivo = CloudinaryField(resource_type="auto", blank=False, null=False)

    def __str__(self):
        return f"{self.tipo} de {self.publicacion.titulo}"
    

    def clean(self):
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


class Comentario(models.Model):
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


class Perfil(models.Model):
    ROLES = (
        ("usuario", "Usuario"),
        ("empresa", "Empresa"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="perfil")
    archivo = CloudinaryField("logo_empresa", resource_type="auto", blank=True, null=True)
    rol = models.CharField(max_length=20, choices=ROLES, default="usuario")

    def __str__(self):
        return f"Perfil de {self.user.username}"

@receiver(post_save, sender=User)
def crear_o_actualizar_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
    else:
        instance.perfil.save()