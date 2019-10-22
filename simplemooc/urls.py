from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from simplemooc.accounts.views import dashboard,user_login,register
from simplemooc.courses.views import index,details
from simplemooc.core.views import home,contact

#admin.autodiscover()

"""urlpatterns = [
    url(r'^$', home, name='core'),
    url(r'^conta/', dashboard, name='accounts'),
    url(r'^cursos/', index, name='courses'),
    url(r'^contato/',contact , name='contatos'),
    url(r'^cursos/detalhaes/',details , name='detalhaes'),
    url(r'^dashboard/',dashboard , name='dashboard'),
    url(r'^registrar/',register, name='dashboard'),
    url(r'^login/',user_login, name='login'),
    url(r'^admin/', admin.site.urls),
    url(r'^logout/', include('django.contrib.auth.urls'), name="logout"),
]"""
urlpatterns = [
    url(r'^', include(('simplemooc.core.urls','core'), namespace='core')),
    url(r'^conta/', include(('simplemooc.accounts.urls','accounts'), namespace='accounts')),
    url(r'^cursos/', include(('simplemooc.courses.urls','courses'), namespace='courses')), 
    #url(r'^sair/', include('django.contrib.auth.urls'), name="logout"),
    url(r'^admin/',admin.site.urls)
]
#if settings.DEBUG:
 #   urlpatterns += static(
  #      settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
   # )
