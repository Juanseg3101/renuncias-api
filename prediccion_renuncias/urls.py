from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Tu aplicación principal con formulario y predicción
    path('', include('predictor.urls')),

    # 👇 Habilita autenticación (login/logout usando Django por defecto)
    path('accounts/', include('django.contrib.auth.urls')),
]
