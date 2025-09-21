from django.db import models

class Animal(models.Model):
    # ...existing code...
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

