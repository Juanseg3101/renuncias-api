import joblib
import os
import json
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import HistorialPrediccion  # 👈 Importar el modelo

# Ruta al modelo
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'voting_model.pkl')
modelo = joblib.load(MODEL_PATH)

# Endpoint API para predicción
@csrf_exempt
def predecir_renuncia(request):
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)

            caracteristicas = [
                datos['satisfaccion'],
                datos['antiguedad'],
                datos['salario_categoria_low'],
                datos['salario_categoria_medium'],
                datos['departamento_IT'],
                datos['departamento_RandD'],
                datos['departamento_Research_and_Development'],
                datos['departamento_Sales'],
                datos['departamento_accounting'],
                datos['departamento_hr'],
                datos['departamento_management'],
                datos['departamento_marketing'],
                datos['departamento_product_mng'],
                datos['departamento_sales'],
                datos['departamento_support'],
                datos['departamento_technical']
            ]

            pred = modelo.predict([caracteristicas])[0]

            if hasattr(modelo, "predict_proba"):
                prob = modelo.predict_proba([caracteristicas])[0][1]
            else:
                prob = 0.0

            return JsonResponse({
                'renunciaria': int(pred),
                'probabilidad': round(prob, 2)
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'mensaje': 'Solo se permiten solicitudes POST'})

# Vista protegida para formulario HTML
@login_required
def formulario_view(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        satisfaccion = float(request.POST.get('satisfaccion'))
        antiguedad = int(request.POST.get('antiguedad'))
        salario = request.POST.get('salario')
        departamento = request.POST.get('departamento')

        # Codificación simple (ajusta si usas OneHot en frontend)
        salario_low = 1 if salario == 'Low' else 0
        salario_medium = 1 if salario == 'Medium' else 0

        # Codificar departamentos
        departamentos = [
            'IT', 'RandD', 'Research_and_Development', 'Sales', 'accounting',
            'hr', 'management', 'marketing', 'product_mng', 'sales', 'support', 'technical'
        ]
        dep_codificados = [1 if departamento == d else 0 for d in departamentos]

        # Construir vector de entrada
        caracteristicas = [satisfaccion, antiguedad, salario_low, salario_medium] + dep_codificados

        # Hacer predicción
        pred = modelo.predict([caracteristicas])[0]

        # Guardar en historial
        HistorialPrediccion.objects.create(
            usuario=request.user,
            satisfaccion=satisfaccion,
            antiguedad=antiguedad,
            salario=salario,
            departamento=departamento,
            resultado=bool(pred)
        )

        # Mostrar resultado
        return render(request, 'predictor/formulario.html', {
            'resultado': pred,
            'mensaje': 'Renunciaría' if pred else 'No renunciaría'
        })

    return render(request, 'predictor/formulario.html')

@login_required
def historial_view(request):
    historial = HistorialPrediccion.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'predictor/historial.html', {'historial': historial})
    
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)  # Inicia sesión automáticamente
            return redirect('formulario')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

from django.db.models import Count
from django.utils.timezone import now

@login_required
def dashboard_view(request):
    # Filtro por usuario actual
    predicciones = HistorialPrediccion.objects.filter(usuario=request.user)

    total = predicciones.count()
    renuncias = predicciones.filter(resultado=True).count()
    no_renuncias = predicciones.filter(resultado=False).count()

    # Agrupación por mes (ejemplo simple)
    por_mes = predicciones.extra({'mes': "strftime('%%Y-%%m', fecha)"}).values('mes').annotate(total=Count('id')).order_by('mes')

    return render(request, 'predictor/dashboard.html', {
        'total': total,
        'renuncias': renuncias,
        'no_renuncias': no_renuncias,
        'por_mes': list(por_mes),
    })
