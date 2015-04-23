from django import forms
from agenda.apps.contactos.models import contacto


class addContactosForm(forms.ModelForm):
	class Meta:
		model = contacto
		exclude = {'status','cliente'}
	
	def __init__(self, *args, **kwargs):
		super(addContactosForm, self).__init__(*args, **kwargs)
		self.fields['categorias'].help_text = ''	
		
'''
class addContactosForm(forms.Form):
	nombre		= forms.CharField(widget=forms.TextInput())
	apellidos	= forms.CharField(widget=forms.TextInput())
	telefono	= forms.CharField(widget=forms.TextInput())
	direccion	= forms.CharField(widget=forms.TextInput())
	correo		= forms.CharField(widget=forms.TextInput())
	descripcion	= forms.CharField(widget=forms.TextInput())
		
	def clean(self):
		return self.cleaned_data

'''
