from django.forms import ModelForm
from App_peliculas.models.criticas import Critica
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class CriticaMF(ModelForm):
    class Meta:
        model = Critica # modelo al que corresponde
        fields = ['email_usuario', 'nombre_usuario', 'puntaje', 'resenia'] # campos que voy a mostrar