from django.contrib import admin
from .models import Animal, Comentario, Publicacion, Consulta, Multimedia, Perfil
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class MultimediaInline(admin.TabularInline):
    model = Multimedia
    extra = 1 
    fields = ("tipo", "archivo")

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_animal', 'raza', 'edad')
    search_fields = ('nombre', 'raza')
    list_filter = ('tipo_animal', 'edad')

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ('animal', 'estado', 'creado')
    search_fields = ('animal__nombre', 'animal__raza')
    list_filter = ('estado', 'animal__tipo_animal', 'animal__raza', 'animal__edad')
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

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = "Perfil"
    fk_name = "user"


class UserAdmin(BaseUserAdmin):
    inlines = (PerfilInline,)
    list_display = ("username", "email", "first_name", "last_name", "is_active", "get_rol")
    list_editable = ("is_active",)
    list_filter = ("is_active", "perfil__rol")

    def get_rol(self, obj):
        return obj.perfil.rol
    get_rol.short_description = "Rol"


# Re-registramos el User con nuestro admin personalizado
admin.site.unregister(User)
admin.site.register(User, UserAdmin)