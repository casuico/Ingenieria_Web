"""
Vistas principales de la aplicación: página de inicio y filtrado de publicaciones.
"""

from django.shortcuts import render
from ..models import Publicacion

def main_page(request):
    """
    Muestra la página principal con todas las publicaciones aprobadas y no adoptadas.
    """
    publicaciones = Publicacion.objects.filter(estado="APR", adoptado=False)
    return render(request, "index.html", {"publicaciones": publicaciones})

