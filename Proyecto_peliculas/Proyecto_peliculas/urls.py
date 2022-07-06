"""Proyecto_peliculas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from App_peliculas.views.home import HomeTV # Aunque lo agrege al __init__.py de views, no me deja hacer el from desde otra ruta más corta
from App_peliculas.views.actores import ActoresTV, ActorDetalleTV
from App_peliculas.views.directores import DirectoresTV, DirectorDetalleTV
from App_peliculas.views.peliculas import PeliculasTV, PeliculaDetalleTV


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeTV.as_view(), name = ''),
    path('home/', HomeTV.as_view(), name = 'home'),
    path('peliculas/', PeliculasTV.as_view(), name = 'peliculas'),
    path('directores/', DirectoresTV.as_view(), name = 'directores'),
    path('actores/', ActoresTV.as_view(), name = 'actores'),
    path('peliculas/detalle/<pk>/', PeliculaDetalleTV.as_view(), name = 'pelicula-detalle'),
    path('directores/detalle/<pk>/', DirectorDetalleTV.as_view(), name = 'director-detalle'),
    path('actores/detalle/<pk>/', ActorDetalleTV.as_view(), name = 'actor-detalle'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

