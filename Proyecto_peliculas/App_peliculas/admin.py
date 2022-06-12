from atexit import register
from django.contrib import admin
from .models import Director, Actor, Pelicula, Critica #, Administrador
from django.utils.html import format_html

# USUARIOS:
# nombre de usuario: administardor
# contraseña: 123

# Register your models here.

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'nacionalidad', 'foto', 'nacimiento', 'biografia') # campos columnas tabla
    list_display_links = ('nombre',) # campo link a editable
    list_filter = ('nacionalidad', 'nacimiento')
    list_per_page = 10 # paginacion
    # fields = ('nombre', 'nacionalidad', 'foto', 'nacimiento', 'biografia') # campos editables. Por defecto: Todos
    ordering = ('id', 'nombre') # criterio de ordenamiento (debe ser una tupla. Puede dejarse: ('nombre',))
    search_fields = ('nombre', 'nacionalidad', 'nacimiento') # tipos de búsquedas soportada
    actions = None # le quito las acciones para que no me aparezca el check box a la izquierda
    
    # NO ME FUNCIONÓ
    # def foto(self, obj):
    #     return format_html('<img src={} width="100" height="100" />', obj.foto.url)


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'nacionalidad', 'foto', 'nacimiento', 'biografia')
    list_display_links = ('nombre',)
    list_filter = ('nacionalidad', 'nacimiento')
    list_per_page = 10
    ordering = ('id', 'nombre')
    search_fields = ('nombre', 'nacionalidad', 'nacimiento')
    actions = None


@admin.register(Pelicula)
class PeliculaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'foto', 'resumen', 'lanzamiento', 'get_actores', 'director', 'puntaje')
    list_display_links = ('nombre',)
    list_filter = ('actores', 'director', 'puntaje', 'lanzamiento')
    list_per_page = 10
    ordering = ('id', 'nombre', 'lanzamiento', 'puntaje')
    search_fields = ('nombre', 'lanzamiento', 'actores', 'director', 'puntaje')
    actions = None

    @admin.display(description='actores', ordering='nombre') # nombre en columna, tabla (sino se ve el "get_actores")
    def get_actores(self, obj):
        return ", ".join([
            actor.nombre for actor in obj.actores.all()
        ])


@admin.register(Critica)
class CriticaAdmin(admin.ModelAdmin):
    list_display = ('id', 'email_usuario', 'nombre_usuario', 'pelicula', 'puntaje', 'resenia', 'resenia_aprobada')
    list_display_links = ('resenia', 'resenia_aprobada')
    list_filter = ('resenia_aprobada',)
    list_per_page = 10
    ordering = ('-id','resenia_aprobada',)
    search_fields = ('email_usuario', 'nombre_usuario')
    actions = None