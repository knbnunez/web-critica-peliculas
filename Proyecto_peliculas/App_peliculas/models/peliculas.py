from tabnanny import verbose
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.contrib import admin
from django.urls import reverse
from .actores import Actor
from .directores import Director
from django.db.models import Q

class PeliculaManager(models.Manager):
    def get_ranking(self):
        return self.order_by('-puntaje')[:12]

class Pelicula(models.Model):
    objects = PeliculaManager()
    nombre = models.CharField(max_length=150)
    #el campo foto no figura explícitamente en Pelicula, pero me pareció conveniente agregarlo
    foto = models.ImageField(null=True, blank=True, upload_to='peliculas/', default='iconos/default_film.png')
    resumen = models.TextField(max_length=300)
    lanzamiento = models.IntegerField()
    actores = models.ManyToManyField(Actor, related_name = 'pelicula')
    director = models.ForeignKey(Director, related_name = 'pelicula', on_delete=models.RESTRICT)
    puntaje = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)]) # para que el get_puntaje tenga efecto hay que cargar a mano una crítica x pelicula con un puntaje X
    
    class Meta:
        verbose_name = ("Pelicula")
        verbose_name_plural = ("Peliculas")

    def __str__(self):
        return self.nombre
    
    def __print_actores(self):
        listado_actores=""
        for actor in self.actores.all():
            listado_actores+=actor.nombre+"; "
        return listado_actores
    
    def __print_director(self):
        return self.director.nombre
    
    def get_descripcion_completa(self):
        return self.nombre+"; "+self.resumen+"; "+str(self.lanzamiento)+"; "+self.__print_actores()+"; "+self.__print_director()+"; "+str(self.puntaje)
     
    def get_puntaje(self):
        sumatoria=0
        cant_puntajes=0
        lista_criticas=self.critica_set.all()
        for c in lista_criticas:
            cant_puntajes+=1
            sumatoria+=c.puntaje
        media=0 if(sumatoria==0) else (sumatoria/cant_puntajes)
        self.puntaje=media
        self.cant_criticas=cant_puntajes # añadido
        self.save()

    cant_criticas = models.IntegerField(default=0) # añadido


@admin.register(Pelicula)
class PeliculaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'puntaje', 'director', 'get_actores', 'lanzamiento', 'resumen', 'foto', )
    list_display_links = ('nombre', )
    list_filter = ('actores', 'director', 'puntaje', 'lanzamiento')
    list_per_page = 10
    ordering = ('nombre', 'lanzamiento', 'puntaje')
    search_fields = ('nombre', 'director__nombre', 'actores__nombre')
    fields = ['nombre', 'foto', 'resumen', 'lanzamiento', 'actores', 'director']
    actions = None

    @admin.display(description='actores', ordering='nombre') # nombre en columna, tabla (sino se ve el "get_actores")
    def get_actores(self, obj):
        return ", ".join([
            actor.nombre for actor in obj.actores.all()
        ])

    from django.contrib.auth.models import Group
    admin.site.unregister(Group) # saco del panel app Grupos, me interesa que se vea solo la de usuarios