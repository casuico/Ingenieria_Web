from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField  # Compatible con SQLite y Postgres

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
    raza = models.CharField(max_length=50, blank=False, null=False)
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
    hogar_actual = models.CharField(max_length=100)
    condiciones_adopcion = models.TextField(blank=False, null=False)

    # Multimedia
    imagen = models.ImageField(upload_to='imagenes_animales/', blank=False, null=False)

    # Información adicional
    historia = models.TextField(blank=True, null=True)
    recomendaciones_cuidado = models.TextField(blank=True, null=True)
    contacto = models.CharField(max_length=100)

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
