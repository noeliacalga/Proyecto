from django.db import models
from django.contrib.auth.models import User


class categoriaContacto(models.Model):
	nombre 	= models.CharField(max_length=200)
	descripcion = models.TextField(max_length=400)
	def __unicode__(self):
		return self.nombre
		

class contacto(models.Model): 
	def url(self,filename):
		ruta = "MultimediaData/Contacto/%s/%s"%(self.nombre,str(filename))
		return ruta

	def foto(self):
		return '<a href="/media/%s"><img src="/media/%s" width=100px heigth=100px/></a>'%(self.imagen,self.imagen)    

	foto.allow_tags=True 

	nombre		= models.CharField(max_length=100)
	apellidos	= models.CharField(max_length=200)
	fecha_nacimiento = models.DateTimeField()
	telefono	= models.CharField(max_length=9)
	direccion	= models.CharField(max_length=200)
	correo		= models.CharField(max_length=200)
	imagen 		= models.ImageField(upload_to=url,null=True,blank=True)
	descripcion	= models.TextField(max_length=300)
	cliente		= models.ForeignKey(User,null=True,blank=True)
	status      = models.BooleanField(default=True)
	categorias	= models.ManyToManyField(categoriaContacto,null=True,blank=True, help_text="") 
	
	def __unicode__(self):
        	return self.nombre

