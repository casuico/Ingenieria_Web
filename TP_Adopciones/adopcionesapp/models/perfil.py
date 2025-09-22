"""
Modelo Perfil para almacenar información adicional de los usuarios.
"""

from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    """
    Modelo que extiende la información del usuario con datos adicionales y rol.
    """
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
    """
    Señal para crear o actualizar el perfil automáticamente al crear o guardar un usuario.
    """
    if created:
        Perfil.objects.create(user=instance)
    else:
        instance.perfil.save()
