from django.conf.urls import include, url
from simplemooc.courses import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/$' ,views.create, name='create'),
    # url(r'^(?P<pk>\d+)/$', 'details', name='details'),
    url(r'^(?P<slug>[\w_-]+)/$', views.details, name='details'),
    url(r'^(?P<slug>[\w_-]+)/inscricao/$', views.enrollment, name='enrollment'),
    url(r'^(?P<slug>[\w_-]+)/cancelar-inscricao/$', views.undo_enrollment,
        name='undo_enrollment'),
    url(r'^(?P<slug>[\w_-]+)/anuncios/$', views.announcements,
        name='announcements'),

    url(r'^(?P<slug>[\w_-]+)/forum/$', views.forum, name='forum'),
    url(r'^(?P<slug>[\w_-]+)/criar-aula/$', views.create_aula, name='create_aula'),

    url(r'^(?P<slug>[\w_-]+)/criar-material/$', views.create_material, name='create_material'),


    url(r'^(?P<slug>[\w_-]+)/anuncios/(?P<pk>\d+)/$', views.show_announcement,
        name='show_announcement'),
    url(r'^(?P<slug>[\w_-]+)/aulas/$', views.lessons, name='lessons'),
    url(r'^(?P<slug>[\w_-]+)/aulas/(?P<pk>\d+)/$', views.lesson, name='lesson'),
    url(r'^(?P<slug>[\w_-]+)/materiais/(?P<pk>\d+)/$', views.material, name='material')
]
