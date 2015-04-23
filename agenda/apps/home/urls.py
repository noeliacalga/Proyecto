from django.conf.urls import patterns,url
urlpatterns = patterns('agenda.apps.home.views',
	url(r"^$",'index_view',name="vista_principal"),
        url(r"^contactos/page/(?P<pagina>.*)/$",'contactos_view',name="vista_contactos"),
	url(r'^contacto/(?P<id_cont>.*)/$','singleContacto_view',name='vista_single_contacto'),
	url(r"^login/$",'login_view',name="vista_login"),
	url(r"^logout/$",'logout_view',name="vista_logout"),
	url(r'^registro/$','register_view',name='vista_registro'),
	url(r'^perfil/(?P<id_cont>.*)/$','perfil_view',name='vista_perfil'),
	
)
