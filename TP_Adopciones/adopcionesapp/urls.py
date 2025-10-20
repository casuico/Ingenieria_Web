"""
Definición de rutas (URLs) para la aplicación adopcionesapp.
"""
from django import views
from django.views.generic import TemplateView
from django.urls import include, path

from .views.auth import editar_perfil
from .views import perfil_usuario, editar_publicacion, filter_publicaciones, main_page, mis_publicaciones, publicaciones_detail, registro, consulta_animal, activar_cuenta, CrearPublicacionView
from .views.rebuild_index import rebuild_index

urlpatterns = [
    path('', main_page, name='main_page'),
    path("publicaciones/<int:pk>/", publicaciones_detail, name='publicaciones_detail'),
    path("registro/", registro, name="registro"),
    path('publicacion/<int:pk>/consulta/', consulta_animal, name='consulta_animal'),
    path("activar/<uidb64>/<token>/", activar_cuenta, name="activar_cuenta"),
    path('publicaciones/crear/', CrearPublicacionView.as_view(), name='crear_publicacion'),
    path('filter-publicaciones/', filter_publicaciones, name='filter_publicaciones'),
    path("publicaciones/<int:pk>/editar/", editar_publicacion, name="editar_publicacion"),
    path("publicaciones/mis_publicaciones/", mis_publicaciones, name="mis_publicaciones"),
    path("perfil/", perfil_usuario, name="perfil_usuario"),
    path("perfil/<int:user_id>/", perfil_usuario, name="perfil_detalle"),
    path('buscar/', include('haystack.urls')),
    path('rebuild_index/', rebuild_index, name='rebuild_index'),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path("perfil/<int:user_id>/", perfil_usuario, name="perfil_usuario"),
    path("perfil/editar/", editar_perfil, name="editar_perfil"),
]