from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.shortcuts import redirect
from django.core import serializers
from django.http import HttpResponse
#from .forms import RegForm, RegModelForm
from .forms import RegModelForm, ContactForm
from django.db.models import Sum
from .models import agencias, asesores, productos,trasacciones

from django.http import JsonResponse

# Create your views here.
def inicio(request):
	titulo = "Bienvenidos"
	context = {
	 	"titulo": "Hola",
	 	}
	if  request.user.is_authenticated() and not request.user.is_staff:
		return redirect('inicio_app')
	else:
		return render(request,"inicio.html",context)

# Create your views here.
def inicio_app(request):
	if request.user.is_authenticated() and not request.user.is_staff:
		usuario = request.user
		context = {
		 	"usuario": usuario,
		}
	else:
            return redirect('inicio')
	return render(request,"system_inicio_general.html",context)
	
def inicio_app_detalles(request):
    if request.user.is_authenticated() and not request.user.is_staff:
        usuario = request.user
        context = {
            "usuario": usuario,
        }
    else:
            return redirect('inicio')
    return render(request,"system_detalles.html",context)

def mapAgencias(request):
    queryset = agencias.objects.all().order_by("id")
    datasource = {}
    datasource ['agencias'] = [] 
    for agencia in queryset:
        data = {}
        data['id'] = agencia.id
        data['age_nombre'] = agencia.age_nombre
        data['age_direccion'] = agencia.age_direccion
        data['age_coordenadax'] = agencia.age_coordenadax
        data['age_coordenaday'] = agencia.age_coordenaday
        datasource ['agencias'].append(data)
    return JsonResponse(datasource)

def todoProductos(request):
    queryset = productos.objects.all().order_by("id")
    datasource = {}
    datasource ['productos'] = [] 
    for producto in queryset:
        data = {}
        data['id'] = producto.id
        data['pro_nombre'] = producto.pro_nombre
        datasource ['productos'].append(data)
    return JsonResponse(datasource)

