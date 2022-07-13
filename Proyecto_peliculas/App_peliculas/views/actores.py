from django.views.generic import TemplateView, ListView
from App_peliculas.models.peliculas import Actor
from App_peliculas.models.peliculas import Pelicula
from django.db.models import Q # Nos ayuda con las consultas
from django.shortcuts import render


class ActoresTV(ListView):
    template_name='actores.html'
    paginate_by = 24
    object_list = Actor.objects.order_by('nombre')
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['actores'] = Actor.objects.all()
        return context

    def get(self, request, *args, **kwargs): # BUSCADOR
        context = self.get_context_data(**kwargs)
        queryset = request.GET.get('query') # <input type="text" name="query" class="form-control" placeholder="Buscar">
        if queryset:
            q = Actor.objects.filter( # filter: puede traer más de un resultado
               Q(nombre__icontains = queryset) |
                Q(nacimiento__icontains = queryset) |
                Q(nacionalidad__icontains = queryset) 
            ).distinct()
            if (q is not None):
                context['encontrado'] = q
                return render(request, "actor_encontrado.html", context=context)
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

    def get(self, request, *args, **kwargs): # BUSCADOR
        context = self.get_context_data(**kwargs)
        queryset = request.GET.get('query') # <input type="text" name="query" class="form-control" placeholder="Buscar">
        if queryset:
            q = Actor.objects.filter( # filter: puede traer más de un resultado
               Q(nombre__icontains = queryset) |
                Q(nacimiento__icontains = queryset) |
                Q(nacionalidad__icontains = queryset) 
            ).distinct()
            if (q is not None):
                context['encontrado'] = q
                return render(request, "actor_encontrado.html", context=context)
        else:
           return self.render_to_response(context)