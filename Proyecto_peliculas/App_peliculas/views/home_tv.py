from django.views.generic.base import TemplateView
from App_peliculas.models import Actor, Director, Pelicula, Critica, PeliculaManager

class HomeTV(TemplateView):
    template_name='index.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['peliculas'] = Pelicula.objects.all()
        context['ranking'] = Pelicula.objects.get_ranking()
        return context

class PeliculasTV(TemplateView):
    template_name='peliculas.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['peliculas'] = Pelicula.objects.all()
        context['criticas'] = Critica.objects.all()
        return context

class DirectoresTV(TemplateView):
    template_name='directores.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['directores'] = Director.objects.all()
        return context

class ActoresTV(TemplateView):
    template_name='actores.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['actores'] = Actor.objects.all()
        return context