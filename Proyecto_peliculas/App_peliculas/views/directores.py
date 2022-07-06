from django.views.generic.base import TemplateView
from App_peliculas.models.peliculas import Director

class DirectoresTV(TemplateView):
    template_name='directores.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['directores'] = Director.objects.all()
        return context

class DirectorDetalleTV(TemplateView):
    template_name='director_detalle.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['directores'] = Director.objects.all()
        return context