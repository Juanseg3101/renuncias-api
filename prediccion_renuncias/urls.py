from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # 🛠 Panel de administración de Django
    path('admin/', admin.site.urls),

    # 🧠 URLs de la app 'predictor' (formulario, predicción, historial, signup)
    path('', include('predictor.urls')),

    # 🔐 Sistema de login/logout con Django Auth (usa templates en /registration/)
    path('accounts/', include('django.contrib.auth.urls')),
]
