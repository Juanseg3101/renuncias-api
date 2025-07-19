import joblib
import os
import json
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

# Ruta al modelo
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'voting_model.pkl')
modelo = joblib.load(MODEL_PATH)

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

            # Validar si el modelo tiene predict_proba
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

# Vista para formulario HTML
def formulario_view(request):
    return render(request, 'predictor/formulario.html')
