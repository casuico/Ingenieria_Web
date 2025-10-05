from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from haystack import connections
from haystack.utils import loading
from .models.publicacion import Publicacion

@receiver(post_save, sender=Publicacion)
def update_publicacion_index(sender, instance, **kwargs):
    backend = connections['default'].get_backend()
    backend.update(loading.get_model('adopcionesapp', 'Publicacion'), [instance])

@receiver(post_delete, sender=Publicacion)
def remove_publicacion_index(sender, instance, **kwargs):
    backend = connections['default'].get_backend()
    backend.remove(instance)