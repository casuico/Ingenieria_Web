"""
Vistas para gestionar las consultas de usuarios sobre publicaciones de animales.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from ..models import Publicacion, Consulta

@login_required
def consulta_animal(request, pk):
    """
    Permite a un usuario autenticado enviar una consulta sobre una publicación.
    Envía un correo electrónico al creador de la publicación con los detalles de la consulta.
    """
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
