from django.contrib import admin
from .models import Publicacion, Consulta

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_animal', 'raza', 'edad')
    search_fields = ('nombre', 'tipo_animal', 'raza', 'edad')
    list_filter = ('nombre', 'tipo_animal', 'raza', 'edad')

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('asunto', 'publicacion', 'usuario', 'nombre', 'email', 'creado')
    search_fields = ('asunto', 'publicacion', 'usuario', 'nombre', 'email', 'creado')
    list_filter = ('asunto', 'publicacion', 'usuario', 'nombre', 'email', 'creado')
