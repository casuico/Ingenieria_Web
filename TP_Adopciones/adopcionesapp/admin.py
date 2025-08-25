from django.contrib import admin
from .models import Comentario, Publicacion, Consulta, Multimedia


class MultimediaInline(admin.TabularInline):  # o admin.StackedInline para más detalle
    model = Multimedia
    extra = 1  # cuántos formularios vacíos mostrar por defecto
    fields = ("tipo", "archivo")  # qué campos mostrar

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_animal', 'raza', 'edad', 'estado')
    search_fields = ('nombre', 'tipo_animal', 'raza', 'edad')
    list_filter = ('nombre', 'tipo_animal', 'raza', 'edad')
    inlines = [MultimediaInline]
    list_editable = ("estado",)

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('asunto', 'publicacion', 'usuario', 'nombre', 'email', 'creado')
    search_fields = ('asunto', 'publicacion', 'usuario', 'nombre', 'email', 'creado')
    list_filter = ('asunto', 'publicacion', 'usuario', 'nombre', 'email', 'creado')

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ("autor", "publicacion", "estado", "creado")
    list_filter = ("estado", "creado")
    search_fields = ("texto", "autor__username", "publicacion__nombre")
    list_editable = ("estado",)