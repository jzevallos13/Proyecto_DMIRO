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

