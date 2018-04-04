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

def fusionLines(request,agencia,anio):
    ##Este arreglo Contendra la lista de los Meses que apareceran en la parte inferior del grafico
    lista_meses = ['Ene', 'Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
    ##Este arreglo contendra sus identidicadores de los meses que corresponden a los codigos de los meses
    ##almacenados en la BD  
    lista_meses_numero = ['1', '2','3','4','5','6','7','8','9','10','11','12']
    ##Este arreglo empezara con datos en 0 que representa que a cada mes np hay datos ingresados,
    ##Una vez llenada esta informacion, estos valores apareceran en el Grafico  
    valores_fusionLines = ['0', '0','0','0','0','0','0','0','0','0','0','0']
    lista_colores = ["#0075c2","#1aaf5d","#d9534f",'#f0ad4e','#0bb39c','#aaad0d','#929c92','#d119d4','#a25822','#39464e']
    datasource = {}
    datasource['chart'] = {}
    datasource['categories'] = []
    datasource['dataset'] = []
    datasource['trendlines'] = []
    query_agencias = agencias.objects.all().filter(id=agencia)
    ##Llenar contenido chart
    datasource['chart'] = {
                "caption": str(query_agencias[0]),
                "subCaption": "Productividad Anual de los Asesores ",
                "captionFontSize": "14",
                "subcaptionFontSize": "14",
                "subcaptionFontBold": "0",
                "paletteColors": lista_colores[0] +","+lista_colores[1]+","+lista_colores[2]+","+lista_colores[3]+","+lista_colores[4]+","+lista_colores[5]+","+lista_colores[6]+","+lista_colores[7]+","+lista_colores[8]+","+lista_colores[9],
                "bgcolor": "#ffffff",
                "showBorder": "0",
                "showShadow": "0",
                "showCanvasBorder": "0",
                "usePlotGradientColor": "0",
                "legendBorderAlpha": "0",
                "legendShadow": "0",
                "showAxisLines": "0",
                "showAlternateHGridColor": "0",
                "divlineThickness": "1",
                "divLineIsDashed": "1",
                "divLineDashLen": "1",
                "divLineGapLen": "1",
                "xAxisName": "Meses",
                "showValues": "0"               
            }     
    #Agregar los Meses
    categories = {}
    categories['category'] = []
    for mes in lista_meses:
        category = {}
        category['label'] = mes
        categories['category'].append(category)
    datasource['categories'].append(categories)
    #Realizar la consulta para determinar cuantos asesores existen
    queryset_asesores = asesores.objects.all().order_by("id")
    #Recorrer todos los asesores
    for asesor in queryset_asesores:
        ##Realizar la consulta a la BD, para traer los resultados
        ##Agrupados por Meses, con sus respectivas sumas, de acuerdo a las 
        ##Agencias,Asesores y Año filtrados
        query = trasacciones.objects.filter(id_agencias_id=agencia,id_asesores_id=asesor.id,tra_anio=anio).values('tra_mes').annotate(suma=Sum('tra_valor')).order_by('tra_mes')
        ##Si la Consulta Existe se procedera a añadir al Asesor
        if query:
            dataset = {}
            dataset['seriesname'] = "ID: "+str(asesor.id) + ", "+"DATOS: " + asesor.ase_nombres +" "+asesor.ase_apellidos           
            dataset['data'] = []
            ##Agregar valoles al arreglo vacio : valores_fusionLines
            ##por cada item que encuentre en la consulta
            for value in query:
                valores_fusionLines[int(value['tra_mes'])-1] = value['suma']
            ##Recorrer el Arreglo: valores_fusionLines, para llenar datos
            ##a los graficos
            for datos in valores_fusionLines:
                data = {}
                data['value'] = datos
                dataset['data'].append(data)    
            ##Insertar datos al dataset recorrido
            datasource['dataset'].append(dataset)    
        ##Vaciar arreglo: valores_fusionLines, para la proxima iteracion
        valores_fusionLines = ['0', '0','0','0','0','0','0','0','0','0','0','0']
    #Agregar los trendlines       
    datasource['trendlines'] = [
                {
                    "line": [
                        {
                            "startvalue": "0",
                            "color": "#6baa01",
                            "valueOnRight": "1",
                            "displayvalue": "Average"
                        }
                    ]
                }
            ]
    return JsonResponse(datasource)

def fusionCircular(request,agencia,asesor,mes):
    lista_meses = ['Enero', 'Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
    query_set = trasacciones.objects.values('id_productos_id__pro_nombre','id_asesores_id__ase_nombres','id_asesores_id__ase_apellidos').annotate(suma=Sum('tra_valor')).filter(id_agencias_id=int(agencia),id_asesores_id=int(asesor),tra_anio=2017,tra_mes=mes).order_by('-suma')
    datos_asesor = ""
    data = []
    sumar = 0
    print(mes)
    for query in query_set:
        datos = {}
        datos['label'] = query['id_productos_id__pro_nombre']
        datos['value'] = query['suma']
        sumar = sumar + query['suma']
        datos_asesor = query['id_asesores_id__ase_nombres'] + " " + query['id_asesores_id__ase_apellidos']
        data.append(datos)
    responseData = {
	"chart": {
                "caption": lista_meses[int(mes)-1] + " del " ,
                "subCaption": datos_asesor,
                "numberPrefix": "$",
                "paletteColors": "#0075c2,#1aaf5d,#f2c500,#f45b00,#8e0000",
                "bgColor": "#ffffff",
                "showBorder": "0",
                "use3DLighting": "0",
                "showShadow": "0",
                "enableSmartLabels": "0",
                "startingAngle": "310",
                "showLabels": "0",
                "showPercentValues": "1",
                "showLegend": "1",
                "legendShadow": "0",
                "legendBorderAlpha": "0",
                "defaultCenterLabel": "$ "+str(sumar),
                "centerLabel": "$label: $value",
                "centerLabelBold": "1",
                "showTooltip": "0",
                "decimals": "0",
                "captionFontSize": "14",
                "subcaptionFontSize": "14",
                "subcaptionFontBold": "0"
            },
            "data": data
}
    return JsonResponse(responseData)

def data(request,agencia):
    ##x = request.GET.get('user', '')
    #zonas = IngresosMeses.objects.all()
    lista = serializers.serialize('json', asesores.objects.all())
    #lista = [{'pk': zona.pk, 'zona': zona.valor} for zona in zonas]
    return HttpResponse(lista,content_type='application/json')

def fusionCircular3DAgencias(request):
    query_set = trasacciones.objects.filter(tra_anio=2017).values('id_agencias_id__age_nombre').annotate(suma=Sum('tra_valor')).order_by('-suma')
    data = []    
    for valores in query_set:
        datos = {}
        datos['label'] = valores['id_agencias_id__age_nombre']
        datos['value'] = valores['suma']
        data.append(datos)
    responseData = {"chart": 
    {
                "caption": "Agencias en General",
                "subCaption": "",
                "numberPrefix": "$",
                "paletteColors": "#0075c2,#1aaf5d,#f2c500,#f45b00,#8e0000",
                "bgColor": "#ffffff",
                "showBorder": "0",
                "use3DLighting": "0",
                "showShadow": "0",
                "enableSmartLabels": "0",
                "startingAngle": "310",
                "showLabels": "0",
                "showPercentValues": "1",
                "showLegend": "1",
                "legendShadow": "0",
                "legendBorderAlpha": "0",                                
                "decimals": "0",
                "captionFontSize": "14",
                "subcaptionFontSize": "14",
                "subcaptionFontBold": "0",
                "toolTipColor": "#ffffff",
                "toolTipBorderThickness": "0",
                "toolTipBgColor": "#000000",
                "toolTipBgAlpha": "80",
                "toolTipBorderRadius": "2",
                "toolTipPadding": "5",
            },
            "data": data
            }
    
    return JsonResponse(responseData)

def fusionCircular3DProductos(request):
    query_set = trasacciones.objects.filter(tra_anio=2017).values('id_productos_id__pro_nombre').annotate(suma=Sum('tra_valor')).order_by('-suma')
    data = []    
    for valores in query_set:
        datos = {}
        datos['label'] = valores['id_productos_id__pro_nombre']
        datos['value'] = valores['suma']
        data.append(datos)
    responseData = {"chart": 
    {
                "caption": "Productos en General",
                "subCaption": "",
                "numberPrefix": "$",
                "paletteColors": "#0075c2,#1aaf5d,#f2c500,#f45b00,#8e0000",
                "bgColor": "#ffffff",
                "showBorder": "0",
                "use3DLighting": "0",
                "showShadow": "0",
                "enableSmartLabels": "0",
                "startingAngle": "310",
                "showLabels": "0",
                "showPercentValues": "1",
                "showLegend": "1",
                "legendShadow": "0",
                "legendBorderAlpha": "0",                                
                "decimals": "0",
                "captionFontSize": "14",
                "subcaptionFontSize": "14",
                "subcaptionFontBold": "0",
                "toolTipColor": "#ffffff",
                "toolTipBorderThickness": "0",
                "toolTipBgColor": "#000000",
                "toolTipBgAlpha": "80",
                "toolTipBorderRadius": "2",
                "toolTipPadding": "5",
            },
            "data": data
            }
    
    return JsonResponse(responseData)

def fusionBarrasProductos(request):
    datasource = {}
    datasource['dataset'] = []
    #Realizar la consulta para determinar cuantos productoes existen
    query_set_agencias = agencias.objects.all().order_by("id")
    #Recorrer todos los productoes
    contador = 0
    for agencia in query_set_agencias:
        ##Realizar la consulta a la BD, para traer los resultados
        ##Agrupados por Meses, con sus respectivas sumas, de acuerdo a las 
        ##Agencias,productoes y Año filtrados
        query = trasacciones.objects.filter(id_agencias_id=agencia.id,tra_anio=2017).values('tra_mes','id_agencias_id','id_productos_id','id_productos_id__pro_nombre').annotate(suma=Sum('tra_valor')).order_by('tra_mes','id_productos_id')
        ##Si la Consulta Existe se procedera a añadir al producto
        if query:
            dataset = {}
            dataset['seriesname'] = agencia.age_nombre
            contador = contador + 1
            dataset['data'] = []
            for datos in query:
                data = {}
                data['value'] = datos
                dataset['data'].append(data)    
            ##Insertar datos al dataset recorrido
            datasource['dataset'].append(dataset)    
    return JsonResponse(datasource)

def fusionLinesGeneral(request):
    ##Este arreglo Contendra la lista de los Meses que apareceran en la parte inferior del grafico
    lista_meses = ['Ene', 'Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']
    ##Este arreglo contendra sus identidicadores de los meses que corresponden a los codigos de los meses
    ##almacenados en la BD  
    lista_meses_numero = ['1', '2','3','4','5','6','7','8','9','10','11','12']
    ##Este arreglo empezara con datos en 0 que representa que a cada mes np hay datos ingresados,
    ##Una vez llenada esta informacion, estos valores apareceran en el Grafico  
    valores_fusionLines = [ 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ]
    datasource = {}
    datasource['categories'] = []
    datasource['dataset'] = []  
    #Agregar los Meses
    categories = {}
    categories['category'] = []
    for mes in lista_meses:
        category = {}
        category['label'] = mes
        categories['category'].append(category)
    datasource['categories'].append(categories)
    #Realizar la consulta para determinar cuantos asesores existen
    queryset_asesores = asesores.objects.all().order_by("id")
    #Recorrer todos los asesores
    agencia_nombre = ""
    for asesor in queryset_asesores:
        ##Realizar la consulta a la BD, para traer los resultados
        ##Agrupados por Meses, con sus respectivas sumas, de acuerdo a las 
        ##Agencias,Asesores y Año filtrados
        query = trasacciones.objects.filter(id_asesores_id=asesor.id,tra_anio=2017).values('tra_mes','id_agencias_id__age_nombre').annotate(suma=Sum('tra_valor')).order_by('tra_mes')
        ##Si la Consulta Existe se procedera a añadir al Asesor
        if query:
            dataset = {}
            #dataset['seriesname'] = "Asesor: " + asesor.ase_nombres +" "+asesor.ase_apellidos           
            dataset['data'] = []
            ##Agregar valoles al arreglo vacio : valores_fusionLines
            ##por cada item que encuentre en la consulta
            for value in query:
                agencia_nombre = value['id_agencias_id__age_nombre']
                valores_fusionLines[int(value['tra_mes'])-1] = value['suma']
            ##Recorrer el Arreglo: valores_fusionLines, para llenar datos
            ##a los graficos
            dataset['seriesname'] = "Asesor: " + asesor.ase_nombres +" "+asesor.ase_apellidos+", "+"Agencia: "+ agencia_nombre  
            #dataset['seriesname'] += " Agencia: "+ agencia_nombre
            for datos in valores_fusionLines:
                data = {}
                data['value'] = datos
                dataset['data'].append(data)    
            ##Insertar datos al dataset recorrido
            datasource['dataset'].append(dataset)    
        ##Vaciar arreglo: valores_fusionLines, para la proxima iteracion
        valores_fusionLines = [ 0, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ]    
    return JsonResponse(datasource)

def contact(request):
	titulo = "Contacto"
	form = ContactForm(request.POST or None)
	if form.is_valid():
		form_email = form.cleaned_data.get("email")
		form_mensaje = form.cleaned_data.get("mensaje")
		from_nombre = form.cleaned_data.get("nombre")
		asunto = 'Form de Contacto'
		email_from = settings.EMAIL_HOST_USER
		email_to = [email_from,"jzevallo@espol.edu.ec"]
		emai_mensaje = "%s: %s enviado por %s" %(from_nombre,form_mensaje,form_email)
		send_mail(asunto,
				emai_mensaje,
				email_from,
				[email_to],
				fail_silently=False)
		#print (email, nombre, mensaje)
	context = {
	 			"form": form,
	 			"titulo":titulo,
		}
	return render(request,"forms.html",context)
