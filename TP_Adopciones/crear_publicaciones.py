import os
import django

# Configurar settings de Django antes de cualquier importación de modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adopciones_project.settings')
django.setup()

from adopcionesapp.models import Publicacion


# Eliminar publicaciones existentes
Publicacion.objects.all().delete()


# Crear 5 publicaciones
Publicacion.objects.create(
    nombre="Firulais",
    tipo_animal="Perro",
    raza="Mestizo",
    edad=3,
    sexo="M",
    castrado=True,
    enfermedades="",
    vacunas=["Rabia", "Moquillo", "Parvovirus"],
    compatibilidad_otros_animales=True,
    compatibilidad_ninos=True,
    comportamiento="Amigable con niños y otros perros",
    hogar_actual="Refugio Municipal",
    condiciones_adopcion="Debe tener espacio para correr y paseos diarios",
    historia="Rescatado de la calle",
    recomendaciones_cuidado="Alimentación balanceada y paseos diarios",
    contacto="contacto@refugio.com"
)

Publicacion.objects.create(
    nombre="Michi",
    tipo_animal="Gato",
    raza="Siames",
    edad=2,
    sexo="H",
    castrado=False,
    enfermedades="",
    vacunas=["Leucemia Felina", "Rabia"],
    compatibilidad_otros_animales=True,
    compatibilidad_ninos=True,
    comportamiento="Cariñoso y juguetón",
    hogar_actual="Refugio Municipal",
    condiciones_adopcion="Necesita espacio interior y compañía",
    historia="Adoptado temporalmente por familia",
    recomendaciones_cuidado="Proporcionar rascadores y juguetes",
    contacto="contacto@refugio.com"
)

Publicacion.objects.create(
    nombre="Conejito Saltarín",
    tipo_animal="Conejo",
    raza="Enano",
    edad=1,
    sexo="M",
    castrado=False,
    enfermedades="Alergia a ciertos alimentos",
    vacunas=["Mixomatosis"],
    compatibilidad_otros_animales=True,
    compatibilidad_ninos=False,
    comportamiento="Muy activo y curioso",
    hogar_actual="Refugio Municipal",
    condiciones_adopcion="Requiere jaula amplia y supervisión diaria",
    historia="Rescatado de granja",
    recomendaciones_cuidado="Atención diaria y alimentación específica",
    contacto="contacto@refugio.com"
)

Publicacion.objects.create(
    nombre="Luna",
    tipo_animal="Perro",
    raza="Labrador",
    edad=4,
    sexo="H",
    castrado=True,
    enfermedades="",
    vacunas=["Rabia", "Hepatitis Canina"],
    compatibilidad_otros_animales=True,
    compatibilidad_ninos=True,
    comportamiento="Tranquila y sociable",
    hogar_actual="Hogar Temporal",
    condiciones_adopcion="Necesita patio y compañía diaria",
    historia="Rescatada de abandono",
    recomendaciones_cuidado="Ejercicios diarios y paseos",
    contacto="contacto@refugio.com"
)

Publicacion.objects.create(
    nombre="Simba",
    tipo_animal="Gato",
    raza="Maine Coon",
    edad=3,
    sexo="M",
    castrado=True,
    enfermedades="",
    vacunas=["Rabia", "Leucemia Felina"],
    compatibilidad_otros_animales=True,
    compatibilidad_ninos=True,
    comportamiento="Curioso y juguetón",
    hogar_actual="Refugio Municipal",
    condiciones_adopcion="Espacio amplio y cariño",
    historia="Encontrado en la calle",
    recomendaciones_cuidado="Juguetes y rascadores",
    contacto="contacto@refugio.com"
)

print("Se eliminaron las publicaciones existentes y se crearon 5 nuevas con la misma imagen")
