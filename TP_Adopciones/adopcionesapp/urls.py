from django.urls import path
from .views import filter_publicaciones, main_page, publicaciones_detail, registro, consulta_animal, activar_cuenta, CrearPublicacionView

urlpatterns = [
    path('', main_page, name='main_page'),
    #path("publicaciones/", publicaciones_list),
    path("publicaciones/<int:pk>/", publicaciones_detail, name='publicaciones_detail'),
    path("registro/", registro, name="registro"),
    path('publicacion/<int:pk>/consulta/', consulta_animal, name='consulta_animal'),
    path("activar/<uidb64>/<token>/", activar_cuenta, name="activar_cuenta"),
    path('publicaciones/crear/', CrearPublicacionView.as_view(), name='crear_publicacion'),
    path('filter-publicaciones/', filter_publicaciones, name='filter_publicaciones'), 
]