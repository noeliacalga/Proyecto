from django.conf.urls import patterns,url

urlpatterns = patterns('agenda.apps.contactos.views',
	url(r'^add/contacto/$','add_contactos_view', name="vista_agregar_contacto"),
	url(r'^edit/contacto/(?P<id_cont>.*)/$','edit_contactos_view',name= "vista_editar_contacto"),
	url(r'^search/$','search_view',name='vista_search'),
	url(r'^edit/perfil/(?P<id_cont>.*)/$','edit_perfil_view',name= "vista_editar_perfil"),
)
