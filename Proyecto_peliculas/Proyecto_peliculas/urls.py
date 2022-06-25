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
from App_peliculas.views.home_tv import HomeTV # Aunque lo agrege al __init__.py de views, no me deja hacer el from desde otra ruta más corta
from App_peliculas.views.actores_tv import ActoresTV
from App_peliculas.views.directores_tv import DirectoresTV
from App_peliculas.views.peliculas_tv import PeliculasTV

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeTV.as_view()),
    path('home', HomeTV.as_view()),
    path('peliculas', PeliculasTV.as_view()),
    path('directores', DirectoresTV.as_view()),
    path('actores', ActoresTV.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

