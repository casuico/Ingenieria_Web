"""
Vistas para la gestión de publicaciones: detalle, creación, edición y listado de publicaciones del usuario.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Publicacion, Multimedia
from ..forms import AnimalForm, ComentarioForm, PublicacionEditarForm, PublicacionForm, MultimediaForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ValidationError

def publicaciones_detail(request, pk):
    """
    Muestra el detalle de una publicación, incluyendo los comentarios aprobados.
    Permite agregar un comentario si el usuario está autenticado.
    """
    publicacion = get_object_or_404(Publicacion, pk=pk)
    comentarios = publicacion.comentarios.filter(estado="aprobado").order_by("-creado")

    if request.method == "POST":
        if request.user.is_authenticated:
            form = ComentarioForm(request.POST)
            if form.is_valid():
                comentario = form.save(commit=False)
                comentario.publicacion = publicacion
                comentario.autor = request.user
                comentario.estado = "pendiente"
                comentario.save()
                messages.success(request, f"Tu comentario será revisado.")
                return redirect("publicaciones_detail", pk=pk)
        else:
            form = ComentarioForm(request.POST)
    else:
        form = ComentarioForm()

    return render(request, "publicaciones_detail.html", {
        "publicacion": publicacion,
        "comentarios": comentarios,
        "comentario_form": form,
    })

class CrearPublicacionView(LoginRequiredMixin, View):
    """
    Vista basada en clase para crear una nueva publicación de adopción.
    Permite cargar datos del animal, la publicación y archivos multimedia.
    """
    def get(self, request):
        return render(
            request,
            "crear_publicacion.html",
            {
                "publicacion_form": PublicacionForm(),
                "animal_form": AnimalForm(),
                "multimedia_form": MultimediaForm(),
            },
        )

    def post(self, request):
        publicacion_form = PublicacionForm(request.POST)
        animal_form = AnimalForm(request.POST)
        multimedia_form = MultimediaForm(request.POST, request.FILES)

        if publicacion_form.is_valid() and animal_form.is_valid() and multimedia_form.is_valid():
            animal = animal_form.save()

            publicacion = publicacion_form.save(commit=False)
            publicacion.creador = request.user
            publicacion.estado = "REV"
            publicacion.animal = animal
            publicacion.save()

            content_type_map = {"image": "imagen", "video": "video"}
            for archivo in multimedia_form.cleaned_data["archivos"]:
                tipo = content_type_map.get(archivo.content_type.split("/")[0], "imagen")
                multimedia = Multimedia(
                    publicacion=publicacion,
                    archivo=archivo,
                    tipo=tipo,
                )
                try:
                    multimedia.full_clean()
                    multimedia.save()
                except ValidationError as e:
                    multimedia_form.add_error(None, e.messages)
                    publicacion.delete()
                    animal.delete()
                    return render(
                        request,
                        "crear_publicacion.html",
                        {
                            "publicacion_form": publicacion_form,
                            "animal_form": animal_form,
                            "multimedia_form": multimedia_form,
                        },
                    )
            messages.success(
                request,
                "Tu publicación fue creada correctamente y será revisada por un administrador."
            )
            return redirect("main_page")

        return render(
            request,
            "crear_publicacion.html",
            {
                "publicacion_form": publicacion_form,
                "animal_form": animal_form,
                "multimedia_form": multimedia_form,
            },
        )

@login_required
def mis_publicaciones(request):
    """
    Muestra todas las publicaciones creadas por el usuario autenticado.
    Permite marcar una publicación como adoptada o no adoptada.
    """
    if request.method == "POST":
        pub_id = request.POST.get("publicacion_id")

        publicacion = request.user.publicaciones.get(pk=pub_id)
        publicacion.adoptado = not publicacion.adoptado
        publicacion.save()
        messages.success(request, f"La publicación {publicacion.titulo} fue marcado como adoptado.")
        return redirect("/")

    publicaciones = request.user.publicaciones.all()
    return render(request, "mis_publicaciones.html", {"publicaciones": publicaciones})

@login_required
def editar_publicacion(request, pk):
    """
    Permite al usuario autenticado editar una publicación propia y su animal asociado.
    Permite agregar archivos multimedia adicionales.
    """
    publicacion = get_object_or_404(Publicacion, pk=pk, creador=request.user)
    animal = publicacion.animal

    if request.method == "POST":
        publicacion_form = PublicacionEditarForm(request.POST, instance=publicacion)
        animal_form = AnimalForm(request.POST, instance=animal)
        multimedia_form = MultimediaForm(request.POST, request.FILES, publicacion=publicacion)

        if publicacion_form.is_valid() and animal_form.is_valid() and multimedia_form.is_valid():
            animal_form.save()
            publicacion_form.save()

            content_type_map = {"image": "imagen", "video": "video"}
            for archivo in multimedia_form.cleaned_data.get("archivos", []):
                tipo = content_type_map.get(archivo.content_type.split("/")[0], "imagen")
                Multimedia.objects.create(
                    publicacion=publicacion,
                    archivo=archivo,
                    tipo=tipo
                )

            messages.success(request, "Tu publicación fue actualizada correctamente.")
            return redirect("mis_publicaciones")
    else:
        publicacion_form = PublicacionEditarForm(instance=publicacion)
        animal_form = AnimalForm(instance=animal)
        multimedia_form = MultimediaForm()

    return render(
        request,
        "editar_publicacion.html",
        {
            "publicacion_form": publicacion_form,
            "animal_form": animal_form,
            "multimedia_form": multimedia_form,
            "publicacion": publicacion
        }
    )

def filter_publicaciones(request):
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

    # Loguear los IDs y títulos de las publicaciones filtradas
    print("Publicaciones filtradas:", list(publicaciones.values_list("id", "titulo")))

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "partials/publicaciones_list.html", {"publicaciones": publicaciones})

    # Si no es AJAX, redirigimos a la página principal
    return render(request, "index.html", {"publicaciones": publicaciones})
