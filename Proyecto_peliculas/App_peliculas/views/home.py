from django.views.generic.base import TemplateView
from App_peliculas.models.peliculas import Pelicula

class HomeTV(TemplateView):
    template_name='index.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['peliculas'] = Pelicula.objects.all()
        context['ranking'] = Pelicula.objects.get_ranking()
        context['peli_carousel_1'] = Pelicula.objects.order_by('-puntaje')[0:1]
        context['peli_carousel_2'] = Pelicula.objects.order_by('-puntaje')[1:2]
        context['peli_carousel_3'] = Pelicula.objects.order_by('-puntaje')[2:3]
        context['peli_carousel_4'] = Pelicula.objects.order_by('-puntaje')[3:4]
        return context