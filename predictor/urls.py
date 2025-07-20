from django.urls import path
from .views import (
    predecir_renuncia,
    formulario_view,
    historial_view,
    signup_view,
    dashboard_view,
    exportar_csv_view  # ✅ NUEVA vista: exportación a CSV
)

urlpatterns = [
    path('predecir/', predecir_renuncia, name='predecir_renuncia'),  # API para predicción
    path('', formulario_view, name='formulario'),                    # Página principal con formulario
    path('historial/', historial_view, name='historial'),            # Historial de predicciones
    path('signup/', signup_view, name='signup'),                     # Registro de nuevos usuarios
    path('dashboard/', dashboard_view, name='dashboard'),            # 📊 Dashboard estadístico
    path('exportar_csv/', exportar_csv_view, name='exportar_csv'),   # 📤 Exportar historial a CSV
]
