from django import forms
from .models import Registrado

class RegModelForm(forms.ModelForm):
	class Meta:
		model = Registrado
		fields = ["nombre","email"]#los campos que quiero ver
##self es la instancia de la clase, en nuestro caso el campo email del formulario
	def clean_email(self):
		email = self.cleaned_data.get("email")
		email_base, proveedor = email.split("@")
		dominio, extension = proveedor.split(".")
		if not extension == "edu":
			raise forms.ValidationError("Por favor utiliza el email .EDU")
		return email

	def clean_nombre(self):
		nombre = self.cleaned_data.get("nombre")
		return nombre

class ContactForm(forms.Form):
	nombre = forms.CharField(required=False)
	email = forms.EmailField()
	mensaje = forms.CharField(widget=forms.Textarea)

#class RegForm(forms.Form):
#	nombre = forms.CharField(max_length=100)
#	email = forms.EmailField()