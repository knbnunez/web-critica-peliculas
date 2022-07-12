from django.views.generic.base import TemplateView
from App_peliculas.models.peliculas import Director
from App_peliculas.models.peliculas import Pelicula
from django.db.models import Q # Nos ayuda con las consultas
from django.shortcuts import render


class DirectoresTV(TemplateView):
    template_name='directores.html'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['directores'] = Director.objects.all()
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


class DirectorDetalleTV(TemplateView):
    template_name='director_detalle.html'
    
    def get_context_data(self, **kwargs):
        pk_director = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['director'] = Director.objects.get(pk = pk_director)
        context['peliculas'] = Pelicula.objects.filter(director = pk_director)
        return context