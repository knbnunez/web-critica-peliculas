from audioop import reverse
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from App_peliculas.models.peliculas import Pelicula
from App_peliculas.models.actores import Actor
from App_peliculas.models.directores import Director # Nos ayuda con las consultas
from django.db.models import Q


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

    def get(self, request, *args, **kwargs): # BUSCADOR
        context = self.get_context_data(**kwargs)
        queryset = request.GET.get('query') # <input type="text" name="query" class="form-control" placeholder="Buscar">
        if queryset:
            q = Pelicula.objects.filter( # filter: puede traer más de un resultado
                Q(nombre__icontains = queryset) |
                Q(lanzamiento__icontains = queryset) |
                Q(director__nombre__icontains = queryset) |
                Q(actores__nombre__icontains = queryset) 
            ).distinct()
            if (q is not None):
                context['encontradas'] = q
                return render(request, "peliculas_encontradas.html", context=context)
        else:
           return self.render_to_response(context)

