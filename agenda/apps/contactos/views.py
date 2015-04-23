import datetime
from django.shortcuts import render_to_response
from django.template import RequestContext
from agenda.apps.contactos.forms import addContactosForm
from agenda.apps.home.forms import userProfileForm
from agenda.apps.home.models import userProfile
from agenda.apps.contactos.models import contacto
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required	
def edit_contactos_view(request, id_cont):
    usuario_visita_web = request.user
    info = "iniciado"
    cont = contacto.objects.get(pk=id_cont)
    if usuario_visita_web.id == cont.cliente.id:  # Si es el creador del contacto
        if request.method == "POST":
            form = addContactosForm(request.POST, request.FILES, instance=cont)
            if form.is_valid():
                edit_cont = form.save(commit=False)
                fecha = datetime.datetime.strptime(str(form.cleaned_data['fecha_nacimiento'].date()), '%Y-%d-%m').date()
                print(fecha)
                form.save_m2m()
                edit_cont.fecha_nacimiento = fecha
                edit_cont.status = True
                edit_cont.save()  # Guardamos el objeto
                info = "Correcto"
                return HttpResponseRedirect('/contacto/%s/' % edit_cont.id)
        else:
            form = addContactosForm(instance=cont)
            ctx = {'form': form, 'informacion': info, 'contacto': cont}
            return render_to_response('contactos/edit.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/")

@login_required		
def edit_perfil_view(request,id_cont):
	info = "iniciado"
	perf= userProfile.objects.get(id=id_cont)
	if contacto.cliente == request.user:
		if request.method == "POST":
			form = userProfileForm(request.POST,request.FILES,instance=perf)
			if form.is_valid():
				edit_perf = form.save(commit=False)
				form.save_m2m()
				edit_perf.status = True
				edit_perf.save() # Guardamos el objeto
				info = "Correcto"
				return HttpResponseRedirect('/perfil/%s/' % edit_perf.id)
		else:
			form = userProfileForm(instance=perf)
			ctx = {'form':form,'informacion':info}
			return render_to_response('contactos/editperfil.html',ctx,context_instance=RequestContext(request))
		

@login_required	
def add_contactos_view(request):
	info = ""
	if request.method == "POST":
		
		form = addContactosForm(request.POST,request.FILES)
		
		if form.is_valid():			
			add = form.save(commit=False)
			add.cliente=request.user
			add.status = True
			add.save() # Guardamos la informacion
			form.save_m2m() # Guarda las relaciones de ManyToMany
			info = "Guardado satisfactoriamente"
			return HttpResponseRedirect('/contacto/%s'%add.id)
	else:
		form = addContactosForm()
	ctx = {'form':form,'informacion':info}
	return render_to_response('contactos/addContacto.html',ctx,context_instance=RequestContext(request)) 
	
	
@login_required	
def search_view(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(nombre__icontains=query) |
            Q(apellidos__icontains=query) |
            Q(correo__icontains=query)
        )
        results = contacto.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response("home/search.html", {
        "results": results,
        "query": query,
	"user": request.user
    })
    

'''

def add_contactos_view(request):
	if request.method == "POST":
		form= addContactosForm(request.POST)
		info = "Inicializando"
		if form.is_valid():
			nombre = form.cleaned_data['nombre']
			descripcion = form.cleaned_data['descripcion']
			c = contacto()
			c.nombre= nombre
			c.descripcion = descripcion
			c.status =True
			c.save()
			info = "Se guardo satisfactoriamente"
		else:
			info = "informacion con datos incorrectos"
		form= addContactosForm()
                ctx={'form':form, 'informacion':info}
		return render_to_response('contactos/addContacto.html',ctx,context_instance=RequestContext(request))
	else:
		form= addContactosForm()
		ctx={'form':form}
		return render_to_response('contactos/addContacto.html',ctx,context_instance=RequestContext(request))
'''
# Create your views here.

