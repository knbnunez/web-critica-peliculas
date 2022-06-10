from distutils.command.upload import upload
from logging import CRITICAL
from django.db import models
from django.forms import CharField
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.utils.safestring import mark_safe

# Create your models here.
# LA LÓGICA EN EL MODELO

class Director(models.Model):
    #a todas las clases, django les genera un 'id' automáticamente
    nombre=models.CharField(max_length=100)
    nacionalidad=models.CharField(max_length=100)
    foto=models.ImageField(null=True, blank=True, upload_to='directores/')
    nacimiento=models.DateField()
    biografia=models.CharField(max_length=300)
    def __str__(self):
        return self.nombre
    def get_descripcion_completa(self):
        return self.nombre+"; "+self.nacionalidad+"; "+str(self.nacimiento)+"; "+self.biografia
    

class Actor(models.Model):
    nombre=models.CharField(max_length=100)
    nacionalidad=models.CharField(max_length=100)
    foto=models.ImageField(null=True, blank=True, upload_to='actores/')
    nacimiento=models.DateField()
    biografia=models.CharField(max_length=300)
    def __str__(self):
        return self.nombre
    def get_descripcion_completa(self):
        return self.nombre+"; "+self.nacionalidad+"; "+str(self.nacimiento)+"; "+self.biografia


class PeliculaManager(models.Manager):
    def get_ranking(self):
        return self.order_by('-puntaje')[:12]

class Pelicula(models.Model):
    objects = PeliculaManager()
    nombre=models.CharField(max_length=150)
    #el campo foto no figura explícitamente en Pelicula, pero me pareció conveniente agregarlo
    foto=models.ImageField(null=True, blank=True, upload_to='peliculas/')
    resumen=models.CharField(max_length=300)
    lanzamiento=models.DateField()
    actores=models.ManyToManyField(Actor)
    director=models.ForeignKey(Director, on_delete=models.RESTRICT) # Revisando documentación, y ejemplos de cómo se ve en la base de datos. Llegué a la conclcusión de que lo que almacena en la Tabla Pelicula, en la Columna director, es el director.id
    puntaje=models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    def get_puntaje(self):
        sumatoria=0
        cant_puntajes=0
        # SELECT PUNTAJE
        # FROM CRITICA
        # WHERE PELICULA=SELF.ID
        # lista_puntajes=self.critica_set.all().value_list('puntaje', flat=True)
        lista_criticas=self.critica_set.all()
        # obtener todos los puntajes de las criticas para una pelicula
        for c in lista_criticas:
            cant_puntajes+=1
            sumatoria+=c.puntaje
        # for puntaje in lista_puntajes:
        #     cant_puntajes+=1
        #     sumatoria+=puntaje
        media=0 if(sumatoria==0) else 1 (sumatoria/cant_puntajes)
        # calcular la media
        self.puntaje=round(media)
        self.save()
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
    


class Critica(models.Model):
    email_usuario=models.EmailField(max_length=254)
    nombre_usuario=models.CharField(max_length=100)
    puntaje=models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    resenia=models.CharField(max_length=400)
    resenia_aprobada=models.BooleanField(default=False)
    pelicula=models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        super(Critica, self).save(*args, **kwargs)
        self.pelicula.get_puntaje()
    def __print_pelicula(self):
        return self.pelicula.nombre
    def __print_resenia(self):
        if(self.resenia_aprobada==False):
            return ""
        else:
            return self.resenia
    def __str__(self):
        return self.nombre_usuario
    def get_descripcion_completa(self):
        return self.email_usuario+"; "+self.nombre_usuario+"; "+str(self.puntaje)+"; "+self.__print_resenia()+"; "+self.__print_pelicula()


class Administrador(models.Model):    
    email=models.EmailField(max_length=254)
    password=models.CharField(max_length=50)
    nombre=models.CharField(max_length=100)
    def get_descripcion_completa(self):
        return self.email+"; "+self.nombre
    def __str__(self):
        return self.nombre


#En teoría, creo que falta la configuración de los ImagesField