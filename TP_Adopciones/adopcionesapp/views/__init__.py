"""
Inicialización de las vistas de la aplicación adopcionesapp.
"""

from .main import main_page
from .publicacion import (publicaciones_detail, CrearPublicacionView, mis_publicaciones,
editar_publicacion,  filter_publicaciones)
from .consulta import consulta_animal
from .auth import registro, activar_cuenta, perfil_usuario
