from haystack import indexes
from .models.publicacion import Publicacion

class PublicacionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    titulo = indexes.CharField(model_attr='titulo')
    historia = indexes.CharField(model_attr='historia', null=True)
    condiciones_adopcion = indexes.CharField(model_attr='condiciones_adopcion')
    recomendaciones_cuidado = indexes.CharField(model_attr='recomendaciones_cuidado', null=True)

    def get_model(self):
        return Publicacion

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(estado='APR')