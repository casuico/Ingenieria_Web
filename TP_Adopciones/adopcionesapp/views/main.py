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

def filter_publicaciones(request):
    """
    Filtra las publicaciones según los parámetros recibidos por GET (edad, sexo, raza, castrado).
    Si la petición es AJAX, retorna solo el listado parcial.
    """
    publicaciones = Publicacion.objects.filter(estado="APR", adoptado=False)

    edad = request.GET.get("edad")
    sexo = request.GET.get("sexo")
    raza = request.GET.get("raza")
    castrado = request.GET.get("castrado")

    if edad:
        publicaciones = publicaciones.filter(animal__edad=edad)
    if sexo:
        publicaciones = publicaciones.filter(animal__sexo=sexo)
    if raza:
        publicaciones = publicaciones.filter(animal__raza__icontains=raza)
    if castrado:
        publicaciones = publicaciones.filter(animal__castrado=(castrado.lower() == "true"))

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "partials/publicaciones_list.html", {"publicaciones": publicaciones})

    return render(request, "index.html", {"publicaciones": publicaciones})
