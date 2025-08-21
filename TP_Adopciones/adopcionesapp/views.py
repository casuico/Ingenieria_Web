#from django.shortcuts import render
from django.forms import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from .models import Publicacion, Consulta, Multimedia
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm
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
    publicaciones = Publicacion.objects.filter(estado="APR")
    return render(request, "index.html", {"publicaciones": publicaciones})

def filter_publicaciones(request):
    publicaciones = Publicacion.objects.filter(estado="APR")

    edad = request.GET.get("edad")
    sexo = request.GET.get("sexo")
    raza = request.GET.get("raza")
    castrado = request.GET.get("castrado")

    if edad:
        publicaciones = publicaciones.filter(edad=edad)
    if sexo:
        publicaciones = publicaciones.filter(sexo=sexo)
    if raza:
        publicaciones = publicaciones.filter(raza__icontains=raza)
    if castrado:
        publicaciones = publicaciones.filter(castrado=(castrado.lower() == "true"))

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return render(request, "partials/publicaciones_list.html", {"publicaciones": publicaciones})

    # Si no es AJAX, redirigimos a la página principal
    return render(request, "index.html", {"publicaciones": publicaciones})


def publicaciones_detail(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    return render(request, "publicaciones_detail.html", {"publicacion": publicacion})


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

        return redirect('consulta_animal', pk=publicacion.pk)

    return render(request, "consulta_animal.html", {"publicacion": publicacion})



class CrearPublicacionView(LoginRequiredMixin, View):
    def get(self, request):
        return render(
            request,
            "crear_publicacion.html",
            {
                "publicacion_form": PublicacionForm(),
                "multimedia_form": MultimediaForm(),
            },
        )

    def post(self, request):
        publicacion_form = PublicacionForm(request.POST)
        multimedia_form = MultimediaForm(request.POST, request.FILES)

        if publicacion_form.is_valid() and multimedia_form.is_valid():
            publicacion = publicacion_form.save(commit=False)
            publicacion.creador = request.user
            publicacion.estado = "REV"
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
                    return render(
                        request,
                        "crear_publicacion.html",
                        {
                            "publicacion_form": publicacion_form,
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
                "multimedia_form": multimedia_form,
            },
        )