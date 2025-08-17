#from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Publicacion
from django.contrib.auth.decorators import login_required
from .forms import RegistroForm
from django.contrib.auth import login



# Create your views here.
def main_page(request):
    publicaciones = Publicacion.objects.all()
    return render(request, "index.html", {"publicaciones": publicaciones})

# Detalle protegido
@login_required
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