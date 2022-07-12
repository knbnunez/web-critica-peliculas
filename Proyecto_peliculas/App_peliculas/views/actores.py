from django.views.generic.base import TemplateView
from App_peliculas.models.peliculas import Actor
from App_peliculas.models.peliculas import Pelicula
from django.db.models import Q # Nos ayuda con las consultas
from django.shortcuts import render


class ActoresTV(TemplateView):
    template_name='actores.html'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['actores'] = Actor.objects.all()
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


class ActorDetalleTV(TemplateView):
    template_name='actor_detalle.html'
    
    def get_context_data(self, **kwargs):
        pk_actor = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['actor'] = Actor.objects.get(pk = pk_actor)
        context['peliculas'] = Pelicula.objects.filter(actores = pk_actor)
        return context