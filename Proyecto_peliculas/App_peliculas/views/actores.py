from django.views.generic.base import TemplateView
from App_peliculas.models.peliculas import Actor

class ActoresTV(TemplateView):
    template_name='actores.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['actores'] = Actor.objects.all()
        return context

class ActorDetalleTV(TemplateView):
    template_name='actor_detalle.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['actores'] = Actor.objects.all()
        return context