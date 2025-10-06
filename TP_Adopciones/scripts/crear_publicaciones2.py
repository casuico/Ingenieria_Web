import sys
import os

# Configurar entorno Django antes de cualquier import de modelos o signals
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'adopciones_project.settings')

import django
django.setup()

from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete

from adopcionesapp.models.animal import Animal
from adopcionesapp.models.publicacion import Publicacion
from adopcionesapp.signals import update_publicacion_index, remove_publicacion_index

# Desconectar señales
post_save.disconnect(update_publicacion_index, sender=Publicacion)
post_delete.disconnect(remove_publicacion_index, sender=Publicacion)

# Crear usuario si no existe
user, _ = User.objects.get_or_create(username='admin', defaults={'password': 'admin'})

# Eliminar publicaciones y animales existentes y por favor que anden
Publicacion.objects.all().delete()
Animal.objects.all().delete()
# Datos de prueba
publicaciones = [
    {
        "titulo": "Firulais busca hogar",
        "animal": {
            "nombre": "Firulais",
            "tipo_animal": "Perro",
            "raza": "Mestizo",
            "edad": 3,
            "sexo": "M",
            "castrado": True,
            "enfermedades": "",
            "vacunas": "Rabia, Moquillo, Parvovirus",
            "compatibilidad_otros_animales": True,
            "compatibilidad_ninos": True,
            "comportamiento": "Amigable con niños y otros perros",
        }
    },
    {
        "titulo": "Michi el gato siames en adopción, hogar responsable",
        "animal": {
            "nombre": "Michi",
            "tipo_animal": "Gato",
            "raza": "Siames",
            "edad": 2,
            "sexo": "H",
            "castrado": False,
            "enfermedades": "",
            "vacunas": "Leucemia Felina, Rabia",
            "compatibilidad_otros_animales": True,
            "compatibilidad_ninos": True,
            "comportamiento": "Cariñoso y juguetón",
        }
    },
    {
        "titulo": "Rocky, el guardián de la casa",
        "animal": {
            "nombre": "Rocky",
            "tipo_animal": "Perro",
            "raza": "Rottweiler",
            "edad": 5,
            "sexo": "M",
            "castrado": True,
            "enfermedades": "",
            "vacunas": "Rabia, Parvovirus",
            "compatibilidad_otros_animales": False,
            "compatibilidad_ninos": True,
            "comportamiento": "Protector y leal",
        }
    },
    {
        "titulo": "Luna, la gata traviesa",
        "animal": {
            "nombre": "Luna",
            "tipo_animal": "Gato",
            "raza": "Mestizo",
            "edad": 1,
            "sexo": "H",
            "castrado": False,
            "enfermedades": "",
            "vacunas": "Rabia",
            "compatibilidad_otros_animales": True,
            "compatibilidad_ninos": True,
            "comportamiento": "Muy activa y curiosa",
        }
    },
    {
        "titulo": "Toby, compañero ideal para niños",
        "animal": {
            "nombre": "Toby",
            "tipo_animal": "Perro",
            "raza": "Beagle",
            "edad": 4,
            "sexo": "M",
            "castrado": True,
            "enfermedades": "",
            "vacunas": "Rabia, Moquillo",
            "compatibilidad_otros_animales": True,
            "compatibilidad_ninos": True,
            "comportamiento": "Juguetón y amigable",
        }
    },
]

for pub in publicaciones:
    animal = Animal.objects.create(**pub["animal"])
    Publicacion.objects.create(
        titulo=pub["titulo"],
        estado='APR',
        animal=animal,
        hogar_actual="Refugio Municipal",
        condiciones_adopcion="Solo familias responsables.",
        historia="Rescatado de la calle.",
        recomendaciones_cuidado="Alimentación balanceada y paseos diarios.",
        creador=user
    )

print("¡Se crearon animales y publicaciones de prueba!")

post_save.connect(update_publicacion_index, sender=Publicacion)
post_delete.connect(remove_publicacion_index, sender=Publicacion)