"""intranet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
#from intranet.home import views
from django.conf import settings

urlpatterns = [
    url(r'^$', include('home.urls')),  #'intranet.home.views.index'),
    url(r'^mktg/', include('marketing.urls')),
    url(r'^dadmin/', admin.site.urls),
    url(r'^hr/', include('hr.urls')),
    url(r'^home/', include('home.urls')),
    url(r'^helper/', include('helper.urls')),
    url(r'session_security/', include('session_security.urls')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
]
