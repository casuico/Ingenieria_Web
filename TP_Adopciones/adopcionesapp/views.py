#from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Publicacion
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm
from django.contrib.auth import login
from .models import Consulta
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages



# Create your views here.
def main_page(request):
    publicaciones = Publicacion.objects.all()
    return render(request, "index.html", {"publicaciones": publicaciones})

def publicaciones_detail(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    return render(request, "publicaciones_detail.html", {"publicacion": publicacion})

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # inicia sesión automáticamente
            return redirect("main_page")  # redirige a la página principal
    else:
        form = RegistroForm()
    return render(request, "registro.html", {"form": form})

@login_required
def consulta_animal(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        asunto = request.POST.get("asunto")
        mensaje = request.POST.get("mensaje")

        # Guardar consulta
        Consulta.objects.create(
            publicacion=publicacion,
            usuario=request.user,
            nombre=nombre,
            email=email,
            asunto=asunto,
            mensaje=mensaje
        )

        # Preparar y enviar email
        cuerpo = f"Nombre: {nombre}\nEmail: {email}\n\nMensaje:\n{mensaje}"
        mail = EmailMessage(
            subject=f"Consulta sobre {publicacion.nombre}: {asunto}",
            body=cuerpo,
            from_email=settings.EMAIL_HOST_USER,
            to=[publicacion.creador.email],
            headers={'Reply-To': email}
        )
        mail.send(fail_silently=False)
        return redirect('publicaciones_detail', pk=publicacion.pk)
    
    return render(request, "consulta_animal.html", {"publicacion": publicacion})