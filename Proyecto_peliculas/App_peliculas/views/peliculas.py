from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView
from App_peliculas.models.peliculas import Pelicula
from App_peliculas.models.criticas import Critica
from App_peliculas.models.actores import Actor
from App_peliculas.forms import CriticaMF


class PeliculasTV(TemplateView):
    template_name = 'peliculas.html'
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['peliculas'] = Pelicula.objects.all()
        return context


class PeliculaDetalleTV(TemplateView):
    template_name = 'pelicula_detalle.html'    
    form_class = CriticaMF # ModelForm de críticas, incluido en pelicula_detalle.html
    
    def get_context_data(self, **kwargs):
        p_selected = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['pelicula'] = Pelicula.objects.get(pk = p_selected)
        context['actores'] = Actor.objects.filter(pelicula = p_selected)
        context['criticas'] = Critica.objects.filter(pelicula = p_selected)
        context['form'] = self.form_class
        return context

    def post(self, request, *args, **kwargs):
        p_selected = self.kwargs['pk']
        email = request.POST['email_usuario']
        nombre = request.POST['nombre_usuario']
        puntaje = request.POST['puntaje']
        resenia = request.POST['resenia']
        if (int(puntaje) >= 1 and int(puntaje) <= 5):
            c_new = Critica()
            c_new.email_usuario = email
            c_new.nombre_usuario = nombre
            c_new.puntaje = puntaje
            c_new.resenia = resenia
            if (str(resenia) == ""):
                c_new.estado_resenia = "R" # si la reseña está en blanco la rechazó automáticamente (el puntaje sí es válido igualmente)
            c_new.pelicula = Pelicula.objects.get(pk = p_selected)
            c_new.save()
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        else:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)