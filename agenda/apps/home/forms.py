from django import forms
from agenda.apps.contactos.models import contacto
from agenda.apps.home.models import userProfile
from django.contrib.auth.models import User
class ContactForm(forms.ModelForm):
	class Meta:
		model = contacto
class LoginForm(forms.Form):
	username=forms.CharField(widget=forms.TextInput())
	password=forms.CharField(widget=forms.PasswordInput(render_value=False))

class RegisterForm(forms.Form):
	
	username = forms.CharField(label="Nombre de Usuario",widget=forms.TextInput())
	email    = forms.EmailField(label="Correo Electronico",widget=forms.TextInput())
	password_one = forms.CharField(label="Password",widget=forms.PasswordInput(render_value=False))
	password_two = forms.CharField(label="Confirmar password",widget=forms.PasswordInput(render_value=False))

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			u = User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError('Nombre de usuario ya existe')

	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			u = User.objects.get(email=email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError('Email ya registrado')

	def clean_password_two(self):
		password_one = self.cleaned_data['password_one']
		password_two = self.cleaned_data['password_two']
		if password_one == password_two:
			pass
		else:
			raise forms.ValidationError('Passwords invalidas, no coinciden')


class userProfileForm(forms.ModelForm):
	class Meta:
		model = userProfile				
		exclude = {'user'}
'''
class ContactForm(forms.Form):
	Nombre = forms.CharField(widget=forms.TextInput())
	Apellidos = forms.CharField(widget=forms.TextInput())
	Direccion= forms.CharField(widget=forms.TextInput())
	Correo = forms.EmailField(widget=forms.TextInput())
        Descripcion = forms.CharField(widget=forms.TextInput())
        
'''
