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
	user=request.user	
	perfil=userProfile.objects.get(user=user)
	ctx = {'perfil':perfil, 'user':request.user}
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
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
				
			except:
				mensaje = {"status":"False"}
				return HttpResponse(simplejson.dumps(mensaje),mimetype='application/json')
			
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
	
	usuario = User.objects.get(id=id_cont)
	
	perf= userProfile.objects.get(id=id_cont)
	ctx={'perfil':perf, 'usuario_2':usuario}
	return render_to_response('home/perfil.html',ctx,context_instance=RequestContext(request))
	


	
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
	form = RegisterForm()
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			usuario = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password_one = form.cleaned_data['password_one']
			password_two = form.cleaned_data['password_two']
			u = User.objects.create_user(username=usuario,email=email,password=password_one)
			u.save() # Guardar el objeto
			return render_to_response('home/thanks_register.html',context_instance=RequestContext(request))
		else:
			ctx = {'form':form}
			return 	render_to_response('home/register.html',ctx,context_instance=RequestContext(request))
	ctx = {'form':form}
	return render_to_response('home/register.html',ctx,context_instance=RequestContext(request))




