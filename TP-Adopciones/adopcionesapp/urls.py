from django.urls import path
from .views import main_page, publicaciones_detail, registro

urlpatterns = [
    path('', main_page, name='main_page'),
    #path("publicaciones/", publicaciones_list),
    path("publicaciones/<int:pk>/", publicaciones_detail, name='publicaciones_detail'),
    path("registro/", registro, name="registro"),
]