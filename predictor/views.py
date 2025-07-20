import joblib
import os
import json
import numpy as np
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Count, Q
from django.utils.timezone import now
from datetime import datetime
from .models import HistorialPrediccion

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
            prob = modelo.predict_proba([caracteristicas])[0][1] if hasattr(modelo, "predict_proba") else 0.0

            return JsonResponse({
                'renunciaria': int(pred),
                'probabilidad': round(prob, 2)
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'mensaje': 'Solo se permiten solicitudes POST'})

@login_required
def formulario_view(request):
    if request.method == 'POST':
        satisfaccion = float(request.POST.get('satisfaccion'))
        antiguedad = int(request.POST.get('antiguedad'))
        salario = request.POST.get('salario')
        departamento = request.POST.get('departamento')

        salario_low = 1 if salario == 'Low' else 0
        salario_medium = 1 if salario == 'Medium' else 0

        departamentos = [
            'IT', 'RandD', 'Research_and_Development', 'Sales', 'accounting',
            'hr', 'management', 'marketing', 'product_mng', 'sales', 'support', 'technical'
        ]
        dep_codificados = [1 if departamento == d else 0 for d in departamentos]

        caracteristicas = [satisfaccion, antiguedad, salario_low, salario_medium] + dep_codificados
        pred = modelo.predict([caracteristicas])[0]

        HistorialPrediccion.objects.create(
            usuario=request.user,
            satisfaccion=satisfaccion,
            antiguedad=antiguedad,
            salario=salario,
            departamento=departamento,
            resultado=bool(pred)
        )

        return render(request, 'predictor/formulario.html', {
            'resultado': pred,
            'mensaje': 'Renunciaría' if pred else 'No renunciaría'
        })

    return render(request, 'predictor/formulario.html')

@login_required
def historial_view(request):
    predicciones = HistorialPrediccion.objects.filter(usuario=request.user)

    filtro_resultado = request.GET.get('resultado')
    if filtro_resultado == 'si':
        predicciones = predicciones.filter(resultado=True)
    elif filtro_resultado == 'no':
        predicciones = predicciones.filter(resultado=False)

    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')
    if desde:
        predicciones = predicciones.filter(fecha__date__gte=desde)
    if hasta:
        predicciones = predicciones.filter(fecha__date__lte=hasta)

    predicciones = predicciones.order_by('-fecha')

    return render(request, 'predictor/historial.html', {
        'historial': predicciones,
        'filtro_resultado': filtro_resultado,
        'desde': desde,
        'hasta': hasta,
    })

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('formulario')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def dashboard_view(request):
    predicciones = HistorialPrediccion.objects.filter(usuario=request.user)

    total = predicciones.count()
    renuncias = predicciones.filter(resultado=True).count()
    no_renuncias = predicciones.filter(resultado=False).count()

    por_mes = predicciones.extra({'mes': "strftime('%%Y-%%m', fecha)"}).values('mes').annotate(total=Count('id')).order_by('mes')

    return render(request, 'predictor/dashboard.html', {
        'total': total,
        'renuncias': renuncias,
        'no_renuncias': no_renuncias,
        'por_mes': list(por_mes),
    })
    