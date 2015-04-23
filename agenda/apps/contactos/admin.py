from django.contrib import admin
from agenda.apps.contactos.models import contacto,categoriaContacto

class contactoAdmin(admin.ModelAdmin):
	list_display = ('nombre','foto','apellidos','cliente')
	list_filter = ('nombre','apellidos','cliente')
	search_fields = ['nombre','apellidos']
	fields = ('nombre','apellidos','fecha_nacimiento','descripcion',('telefono','direccion','correo'),'imagen','categorias','cliente','status')

admin.site.register(contacto,contactoAdmin) 
admin.site.register(categoriaContacto)
# Register your models here.
