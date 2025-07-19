from django.urls import path
from .views import predecir_renuncia, formulario_view  # importa ambas vistas

urlpatterns = [
    path('predecir/', predecir_renuncia, name='predecir_renuncia'),
    path('', formulario_view, name='formulario'),  # ruta principal que carga el formulario
]