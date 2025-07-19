from django.urls import path
from .views import (
    predecir_renuncia,
    formulario_view,
    historial_view,
    signup_view  # 👈 NUEVA vista de registro
)

urlpatterns = [
    path('predecir/', predecir_renuncia, name='predecir_renuncia'),  # API para predicción
    path('', formulario_view, name='formulario'),                    # Página principal con formulario
    path('historial/', historial_view, name='historial'),            # Historial de predicciones
    path('signup/', signup_view, name='signup'),                     # Registro de nuevos usuarios
]
