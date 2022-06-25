from django.views.generic.base import TemplateView
from App_peliculas.models.peliculas import Pelicula
from App_peliculas.models.criticas import Critica

class PeliculasTV(TemplateView):
    template_name='peliculas.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['peliculas'] = Pelicula.objects.all()
        context['criticas'] = Critica.objects.all()
        return context