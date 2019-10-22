from django.conf.urls import  include, url
from django.contrib.auth import logout
from django.conf import settings
from simplemooc.accounts import views

urlpatterns = [
    url(r'^$', views.dashboard, 
        name='dashboard'),
    url(r'^entrar/$', views.user_login, name='user_login'),
    url(r'^sair/', include('django.contrib.auth.urls'), name="logout"),

    #url(r'^sair/$', logout, 
     #    name='logout'),
    url(r'^cadastre-se/$', views.register, 
        name='register'),
    url(r'^nova-senha/$', views.password_reset, 
        name='password_reset'),
    url(r'^confirmar-nova-senha/(?P<key>\w+)/$', 
        views.password_reset_confirm, 
        name='password_reset_confirm'),
    url(r'^editar/$', views.edit, 
        name='edit'),
    url(r'^editar-senha/$', views.edit_password, 
        name='edit_password')
]

    #url(r'^logout/', include('django.contrib.auth.urls'), name="logout"),
    #url(r'^login/',user_login, name='login'),
