from django.db import models
from django.contrib import admin

class Director(models.Model):
    #a todas las clases, django les genera un 'id' automáticamente
    nombre=models.CharField(max_length=100)
    nacionalidad=models.CharField(max_length=100)
    foto=models.ImageField(null=True, blank=True, upload_to='directores/', default='iconos/default_profile.png')
    # nacimiento=models.DateField() # solo necesitamos el año
    nacimiento=models.IntegerField()
    biografia=models.TextField(max_length=300)
    
    class Meta:
        verbose_name = ("Director")
        verbose_name_plural = ("Directores")

    def __str__(self):
        return self.nombre
    
    def get_descripcion_completa(self):
        return self.nombre+"; "+self.nacionalidad+"; "+str(self.nacimiento)+"; "+self.biografia

#

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nacimiento', 'nacionalidad', 'biografia', 'foto', ) # campos columnas tabla
    list_display_links = ('nombre',) # campo link a editable
    list_filter = ('nacionalidad', 'nacimiento')
    list_per_page = 10 # paginacion
    # fields = ('nombre', 'nacionalidad', 'foto', 'nacimiento', 'biografia') # campos editables. Por defecto: Todos
    ordering = ('nombre', ) # criterio de ordenamiento (debe ser una tupla. Puede dejarse: ('nombre',))
    search_fields = ('nombre', 'nacionalidad', 'nacimiento') # tipos de búsquedas soportada
    actions = None # le quito las acciones para que no me aparezca el check box a la izquierda
    
    # NO ME FUNCIONÓ
    # def foto(self, obj):
    #     return format_html('<img src={} width="100" height="100" />', obj.foto.url)