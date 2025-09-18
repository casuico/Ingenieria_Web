#from django.shortcuts import render
from django.forms import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from .models import Publicacion, Consulta, Multimedia
from django.contrib.auth.decorators import login_required
from .forms import AnimalForm, ComentarioForm, PublicacionEditarForm, RegistroForm
from django.contrib.auth import login
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from .forms import PublicacionForm, MultimediaForm
from django.contrib.auth.mixins import LoginRequiredMixin




def main_page(request):
    publicaciones = Publicacion.objects.filter(estado="APR", adoptado=False)
    return render(request, "index.html", {"publicaciones": publicaciones})

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

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "partials/publicaciones_list.html", {"publicaciones": publicaciones})

    # Si no es AJAX, redirigimos a la página principal
    return render(request, "index.html", {"publicaciones": publicaciones})


def publicaciones_detail(request, pk):
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


def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            activation_url = f"http://{current_site.domain}/activar/{uid}/{token}/"

            subject = "Activa tu cuenta"
            from_email = settings.EMAIL_HOST_USER
            to_email = form.cleaned_data.get("email")

            text_content = f"Hola {user.username}, haz clic en el enlace para activar tu cuenta: {activation_url}"

            html_content = render_to_string("email_verificacion.html", {
                "user": user,
                "url": activation_url
            })

            # Crear mensaje HTML
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return render(request, "registro_exitoso.html")
    else:
        form = RegistroForm()

    return render(request, "registro.html", {"form": form})


def activar_cuenta(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("main_page")
    else:
        return HttpResponse("El enlace de activación no es válido o ya expiró.")



@login_required
def consulta_animal(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        asunto = request.POST.get("asunto")
        mensaje = request.POST.get("mensaje")

        Consulta.objects.create(
            publicacion=publicacion,
            usuario=request.user,
            nombre=nombre,
            email=email,
            asunto=asunto,
            mensaje=mensaje
        )

        text_content = f"""
        Consulta sobre {publicacion.nombre}

        Nombre: {nombre}
        Email: {email}

        Mensaje:
        {mensaje}
        """

        html_content = render_to_string("consulta_email.html", {
            "publicacion": publicacion,
            "nombre": nombre,
            "email": email,
            "mensaje": mensaje
        })

        msg = EmailMultiAlternatives(
            subject=f"Consulta sobre {publicacion.nombre}: {asunto}",
            body=text_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[publicacion.creador.email],
            headers={'Reply-To': email}
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)

        messages.success(request, f"Tu consulta sobre '{publicacion.nombre}' fue enviada correctamente.")

        return redirect('publicaciones_detail', pk=publicacion.pk)

    return render(request, "consulta_animal.html", {"publicacion": publicacion})



class CrearPublicacionView(LoginRequiredMixin, View):

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

@login_required
def perfil_usuario(request):
    usuario = request.user
    perfil = usuario.perfil

    if request.method == "POST" and perfil.rol == "empresa":
        archivo = request.FILES.get("archivo")
        if archivo:
            perfil.archivo = archivo
            perfil.save()
            messages.success(request, "El logo de la empresa se actualizó correctamente.")
        else:
            messages.error(request, "Debes seleccionar un archivo para subir.")
        return redirect("perfil_usuario")

    return render(request, "perfil_usuario.html", {"usuario": usuario})