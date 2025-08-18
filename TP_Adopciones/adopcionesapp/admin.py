from django.contrib import admin
from .models import Publicacion, Consulta, Multimedia


class MultimediaInline(admin.TabularInline):  # o admin.StackedInline para más detalle
    model = Multimedia
    extra = 1  # cuántos formularios vacíos mostrar por defecto
    fields = ("tipo", "archivo")  # qué campos mostrar

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_animal', 'raza', 'edad')
    search_fields = ('nombre', 'tipo_animal', 'raza', 'edad')
    list_filter = ('nombre', 'tipo_animal', 'raza', 'edad')
    inlines = [MultimediaInline]

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('asunto', 'publicacion', 'usuario', 'nombre', 'email', 'creado')
    search_fields = ('asunto', 'publicacion', 'usuario', 'nombre', 'email', 'creado')
    list_filter = ('asunto', 'publicacion', 'usuario', 'nombre', 'email', 'creado')
