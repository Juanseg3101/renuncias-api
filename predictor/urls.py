from django.urls import path
from .views import predecir_renuncia, formulario_view, historial_view  # 👈 importa todas las vistas

urlpatterns = [
    path('predecir/', predecir_renuncia, name='predecir_renuncia'),  # API
    path('', formulario_view, name='formulario'),                    # Formulario principal
    path('historial/', historial_view, name='historial'),            # Vista del historial
]
