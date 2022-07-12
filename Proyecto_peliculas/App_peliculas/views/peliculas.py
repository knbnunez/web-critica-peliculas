from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView
from App_peliculas.models.peliculas import Pelicula
from App_peliculas.models.criticas import Critica
from App_peliculas.models.actores import Actor
from App_peliculas.forms import CriticaMF
from django.db.models import Q # Nos ayuda con las consultas


class PeliculasTV(ListView): # Catálogo de Peliculas
    template_name = 'peliculas.html'
    paginate_by = 24
    # queryset = Pelicula.objects.order_by('nombre')
    object_list = Pelicula.objects.order_by('nombre')

    def get(self, request, *args, **kwargs): # BUSCADOR
        context = self.get_context_data(**kwargs)
        queryset = request.GET.get('query') # <input type="text" name="query" class="form-control" placeholder="Buscar">
        if queryset:
            q = Pelicula.objects.filter( # filter: puede traer más de un resultado
                Q(nombre__icontains = queryset)
                # | ...
            ).distinct()
            if (q is not None):
                context['encontradas'] = q
                return render(request, "peliculas_encontradas.html", context=context)
        else:
           return self.render_to_response(context)


class PeliculaDetalleTV(TemplateView): # Detalle de una Película
    template_name = 'pelicula_detalle.html'
    # Para las Críticas
    form_class = CriticaMF # ModelForm de críticas, incluido en pelicula_detalle.html
    # model = Critica # 'criticas' será ahora iterable mediante object_list
    # paginate_by = 2

    # def get_queryset(self):
    #     pk_pelicula = self.kwargs['pk']
    #     return Critica.objects.filter(pelicula = pk_pelicula)

    def get_context_data(self, **kwargs):
        pk_pelicula = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        print(context)
        context['pelicula'] = Pelicula.objects.get(pk = pk_pelicula)
        context['actores'] = Actor.objects.filter(pelicula = pk_pelicula)
        context['criticas'] = Critica.objects.filter(pelicula = pk_pelicula)
        # context['criticas'] = self.object_list
        context['form'] = self.form_class
        return context

    def post(self, request, *args, **kwargs):
        pk_pelicula = self.kwargs['pk']
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
            c_new.pelicula = Pelicula.objects.get(pk = pk_pelicula)
            c_new.save()
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        else:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
            
    def get(self, request, *args, **kwargs): # BUSCADOR
        context = self.get_context_data(**kwargs)
        queryset = request.GET.get('query') # <input type="text" name="query" class="form-control" placeholder="Buscar">
        if queryset:
            q = Pelicula.objects.filter( # filter: puede traer más de un resultado
                Q(nombre__icontains = queryset)
                # | ...
            ).distinct()
            if (q is not None):
                context['encontradas'] = q
                return render(request, "peliculas_encontradas.html", context=context)
        else:
           return self.render_to_response(context)


# class CriticasLV(ListView):
#     model = Critica # 'criticas' será ahora iterable mediante object_list
#     template_name = 'criticas.html'
#     form_class = CriticaMF # ModelForm de críticas, incluido en pelicula_detalle.html
#     paginate_by = 5
    
#     def post(self, request, *args, **kwargs):
#             pk_pelicula = self.kwargs['pk']
#             email = request.POST['email_usuario']
#             nombre = request.POST['nombre_usuario']
#             puntaje = request.POST['puntaje']
#             resenia = request.POST['resenia']
#             if (int(puntaje) >= 1 and int(puntaje) <= 5):
#                 c_new = Critica()
#                 c_new.email_usuario = email
#                 c_new.nombre_usuario = nombre
#                 c_new.puntaje = puntaje
#                 c_new.resenia = resenia
#                 if (str(resenia) == ""):
#                     c_new.estado_resenia = "R" # si la reseña está en blanco la rechazó automáticamente (el puntaje sí es válido igualmente)
#                 c_new.pelicula = Pelicula.objects.get(pk = pk_pelicula)
#                 c_new.save()
#                 context = self.get_context_data(**kwargs)
#                 return self.render_to_response(context)
#             else:
#                 context = self.get_context_data(**kwargs)
#                 return self.render_to_response(context)