from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from haystack import connections
from .models import Publicacion

@receiver(post_save, sender=Publicacion) 
def update_publicacion_index(sender, instance, **kwargs):
    backend = connections['default'].get_backend()
    index = connections['default'].get_unified_index().get_index(sender)
    backend.update(index, [instance])

@receiver(post_delete, sender=Publicacion)
def remove_publicacion_index(sender, instance, **kwargs):
    backend = connections['default'].get_backend()
    index = connections['default'].get_unified_index().get_index(sender)
    backend.remove(index, [instance])
