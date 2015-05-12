from django.shortcuts import render_to_response
from django.template import RequestContext
from agenda.apps.contactos.models import contacto
from agenda.apps.home.forms import ContactForm,LoginForm,RegisterForm,userProfileForm
from agenda.apps.home.models import userProfile
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import json as simplejson

def index_view(request):
	
	return render_to_response('home/index.html',context_instance=RequestContext(request))
	
@login_required		
def contactos_view(request,pagina):
	if request.method=="POST":
		
		if "contact_id" in request.POST:
			try:
				id_contacto = request.POST['contact_id']
				p = contacto.objects.get(pk=id_contacto)
				mensaje = {"status":"True","contact_id":p.id}
				p.delete() # Elinamos objeto de la base de datos
				# mimetype ya no se utiliza
				return HttpResponse(simplejson.dumps(mensaje),content_type='application/json')
				
			except:
				mensaje = {"status":"False"}
				return HttpResponse(simplejson.dumps(mensaje),content_type='application/json')
			
	lista_cont = contacto.objects.filter(status=True, cliente= request.user)
	paginator = Paginator(lista_cont,3)
	try:
		page = int(pagina)
	except:
		page= 1
	try:
		contactos= paginator.page(page)
	except (EmptyPage,InvalidPage):
		contactos = paginator.page(paginator.num_pages)
	ctx={'contactos':contactos}
        return render_to_response('home/contactos.html',ctx,context_instance=RequestContext(request))


@login_required
def singleContacto_view(request, id_cont):
    usuario_visita_web = request.user
    cont= contacto.objects.get(id=id_cont)
    if usuario_visita_web.id == cont.cliente.id:  # Si es el creador del contacto
        cats = cont.categorias.all()
        ctx={'contacto':cont, 'categorias':cats}
        return render_to_response('home/SingleContacto.html',ctx,context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/")


@login_required	
def perfil_view(request,id_cont):
	usuario_visita_web = request.user
	usuario = User.objects.get(id=id_cont)
	perf= userProfile.objects.get(user=usuario)
	if usuario_visita_web.id == usuario.id:	
		ctx={'perfil':perf, 'usuario_2':usuario}
		return render_to_response('home/perfil.html',ctx,context_instance=RequestContext(request))
	else:
		return HttpResponseRedirect("/")	


	
def login_view(request):
	mensaje=""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		if request.method == "POST":
			form= LoginForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				usuario = authenticate(username=username,password=password)
				if usuario is not None and usuario.is_active:
					login(request,usuario)
					return HttpResponseRedirect('/')
				else: 
					mensaje= " usuario y/o password incorrecto"
		
		form = LoginForm()
		ctx = {'form':form,'mensaje':mensaje}
		return render_to_response('home/login.html',ctx,context_instance=RequestContext(request))
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def register_view(request):
	form = RegisterForm(prefix='form')
	form2 = userProfileForm(prefix='form2')
	perfil = userProfile()
	if request.method == "POST":
		form = RegisterForm(request.POST, prefix='form')
		form2 = userProfileForm(request.POST, prefix='form2')		
		if form.is_valid() and form2.is_valid():
			usuario = form.cleaned_data['username']			
			password_one = form.cleaned_data['password_one']
			password_two = form.cleaned_data['password_two']
			perfil.apellidos = form2.cleaned_data['apellidos']
			perfil.fecha_nacimiento = form2.cleaned_data['fecha_nacimiento']
			perfil.telefono = form2.cleaned_data['telefono']
			perfil.direccion = form2.cleaned_data['direccion']
			perfil.correo = form2.cleaned_data['correo']
			perfil.photo = form2.cleaned_data['photo']
			perfil.nombre = usuario
			u.email=perfil.correo				
			u = User.objects.create_user(username=usuario,password=password_one)
			u.save() # Guardar el objeto
			perfil.user=u
			perfil.save()					
			print "correcto"
			return render_to_response('home/thanks_register.html',context_instance=RequestContext(request))
		else:
			ctx = {'form':form , 'form2':form2}
			print "error"
			print(form.errors)
			print(form2.errors)	
			return 	render_to_response('home/register.html',ctx,context_instance=RequestContext(request))
	ctx = {'form':form,'form2':form2}
	print "error2"
	return render_to_response('home/register.html',ctx,context_instance=RequestContext(request))




