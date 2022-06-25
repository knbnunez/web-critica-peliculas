from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.contrib import admin
from .peliculas import Pelicula

class Critica(models.Model):
    email_usuario = models.EmailField(max_length=254)
    nombre_usuario = models.CharField(max_length=100)
    puntaje = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    resenia = models.CharField(max_length=400, blank=True, verbose_name="Reseña")
    RESENIA_CHOICES = (
        ("P", "Pendiente"),
        ("A", "Aprobada"),
        ("R", "Rechazada"),
    )
    estado_resenia = models.CharField(max_length=9, choices=RESENIA_CHOICES, default="P", verbose_name="Estado")
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = ("Critica")
        verbose_name_plural = ("Criticas")

    def save(self, *args, **kwargs):
        super(Critica, self).save(*args, **kwargs)
        self.pelicula.get_puntaje()
    
    def __print_pelicula(self):
        return self.pelicula.nombre
    
    def __print_resenia(self):
        if (self.estado_resenia == "Pendiente" or self.estado_resenia == "Rechazada"):
            return ""
        else:
            return self.resenia
    
    def __str__(self):
        return self.nombre_usuario
    
    def get_descripcion_completa(self):
        return self.email_usuario + "; " + self.nombre_usuario + "; " + str(self.puntaje) + "; " + self.__print_resenia() + "; " + self.__print_pelicula()


@admin.register(Critica)
class CriticaAdmin(admin.ModelAdmin):
    list_display = ('estado_resenia', 'resenia', 'email_usuario', 'nombre_usuario', 'pelicula', 'puntaje')
    list_display_links = ('estado_resenia', )
    list_filter = ('estado_resenia', )
    list_per_page = 10
    ordering = ('estado_resenia', )
    search_fields = ('email_usuario', 'nombre_usuario', 'estado_resenia',)
    actions = None
    fields = ['estado_resenia'] # solo la reseña

    def has_add_permission(self, request):
        return False # eliminamos el boton de agregar críticas
    def has_delete_permission(self, request, obj=None):
        return False # y el de elminarlas
