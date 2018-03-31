from django.core.validators import MaxValueValidator
from django.db import models

# Create your models here.
class Registrado(models.Model):
	nombre = models.CharField(max_length=100, blank=False, null=False)
	email = models.EmailField()
	timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)

	def __unicode__(self): #Python2
		return self.nombre
	def __str__(self): #Python3
		return self.nombre

class agencias(models.Model):
	age_nombre = models.CharField(max_length=100, blank=False, null=False)
	age_direccion = models.CharField(max_length=100, blank=False, null=False)
	age_coordenadax = models.CharField(max_length=100, blank=False, null=False)
	age_coordenaday = models.CharField(max_length=100, blank=False, null=False)
	
	def __unicode__(self): #Python2
		return self.age_nombre
	def __str__(self): #Python3
		return self.age_nombre
		# Create your models here.

class asesores(models.Model):
	ase_nombres = models.CharField(max_length=100, blank=False, null=False)
	ase_apellidos = models.CharField(max_length=100, blank=False, null=False)
	def __unicode__(self): #Python2
		return self.ase_nombres
	def __str__(self): #Python3
		return self.ase_nombres

class productos(models.Model):
	pro_nombre = models.CharField(max_length=100, blank=False, null=False)
	def __unicode__(self): #Python2
		return self.pro_nombre
	def __str__(self): #Python3
		return self.pro_nombre

class trasacciones(models.Model):
	id_agencias = models.ForeignKey(agencias, on_delete=models.CASCADE)
	id_asesores = models.ForeignKey(asesores, on_delete=models.CASCADE)
	id_productos = models.ForeignKey(productos, on_delete=models.CASCADE)
	tra_mes = models.CharField(max_length=2, blank=False, null=False)
	tra_anio = models.CharField(max_length=4, blank=False, null=False)
	tra_valor = models.PositiveIntegerField(validators=[MaxValueValidator(10)], blank=False, null=False)

	def __unicode__(self): #Python2
		return self.tra_valor
	def __str__(self): #Python3
		return self.tra_valor