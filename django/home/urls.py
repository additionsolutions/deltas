from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.intra_login, name='intra_login'),
    url(r'^logout/', views.intra_logout, name='intra_logout'),
    url(r'^login_process/', views.login_process, name='login_process'),
    url(r'^mpage/', views.mpage, name='mpage'),
    url(r'^contact/', views.contact, name='contact'),
    url(r'^send_mail/', views.send_mail, name='send_mail'),
	
]
