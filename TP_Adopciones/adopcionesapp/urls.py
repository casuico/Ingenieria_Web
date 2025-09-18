from django.urls import path
from .views import perfil_usuario, editar_publicacion, filter_publicaciones, main_page, mis_publicaciones, publicaciones_detail, registro, consulta_animal, activar_cuenta, CrearPublicacionView

urlpatterns = [
    path('', main_page, name='main_page'),
    #path("publicaciones/", publicaciones_list),
    path("publicaciones/<int:pk>/", publicaciones_detail, name='publicaciones_detail'),
    path("registro/", registro, name="registro"),
    path('publicacion/<int:pk>/consulta/', consulta_animal, name='consulta_animal'),
    path("activar/<uidb64>/<token>/", activar_cuenta, name="activar_cuenta"),
    path('publicaciones/crear/', CrearPublicacionView.as_view(), name='crear_publicacion'),
    path('filter-publicaciones/', filter_publicaciones, name='filter_publicaciones'),
    path("publicaciones/<int:pk>/editar/", editar_publicacion, name="editar_publicacion"),
    path("publicaciones/mis_publicaciones/", mis_publicaciones, name="mis_publicaciones"),
    path("perfil/", perfil_usuario, name="perfil_usuario"),
]