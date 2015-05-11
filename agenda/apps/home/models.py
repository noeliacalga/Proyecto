from django.db import models
from django.contrib.auth.models import User

class userProfile(models.Model):
	def url(self,filename):
		ruta = "MultimediaData/Users/%s/%s"%(self.user.username,filename)
		return ruta
	user = models.OneToOneField(User)	
	nombre		= models.CharField(max_length=100)
	apellidos	= models.CharField(max_length=200)
	fecha_nacimiento = models.DateTimeField()
	telefono	= models.CharField(max_length=9)
	direccion	= models.CharField(max_length=200)
	correo		= models.CharField(max_length=200)
	photo 		= models.ImageField(upload_to=url,null=True, blank=True)
	
	USERNAME_FIELD = 'nombre'
	def __unicode__(self):
		return self.user.username

# Create your models here.
