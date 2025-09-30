"""
Vistas relacionadas con la autenticación de usuarios, registro, activación de cuenta y perfil.
"""

from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..forms import RegistroForm

def registro(request):
    """
    Vista para el registro de nuevos usuarios.
    Envía un correo de activación al usuario registrado.
    """
    if request.method == "POST":
        try:
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
                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = form.cleaned_data.get("email")

                text_content = f"Hola {user.username}, haz clic en el enlace para activar tu cuenta: {activation_url}"

                html_content = render_to_string("email_verificacion.html", {
                    "user": user,
                    "url": activation_url
                })

                msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                return render(request, "registro_exitoso.html")
        except Exception as e:
            print(f"Error al enviar el correo: {e}")
    else:
        form = RegistroForm()

    return render(request, "registro.html", {"form": form})

def activar_cuenta(request, uidb64, token):
    """
    Vista para activar la cuenta de usuario a través del enlace enviado por correo.
    Si el token es válido, activa la cuenta y realiza login automático.
    """
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
def perfil_usuario(request, user_id=None):
    """
    Vista para mostrar y actualizar el perfil del usuario.
    """
    if user_id:
        usuario = get_object_or_404(User, pk=user_id)
    else:
        usuario = request.user

    perfil = usuario.perfil
    publicaciones = usuario.publicaciones.all()

    if request.method == "POST" and perfil.rol == "empresa" and usuario == request.user:
        archivo = request.FILES.get("archivo")
        if archivo:
            perfil.archivo = archivo
            perfil.save()
            messages.success(request, "El logo de la empresa se actualizó correctamente.")
        else:
            messages.error(request, "Debes seleccionar un archivo para subir.")
        return redirect("perfil_usuario")

    return render(request, "perfil_usuario.html", {
        "usuario": usuario,
        "publicaciones": publicaciones,
    })