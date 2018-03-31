"""dmiro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from appdmiro import views
#from .views import about

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^$', views.inicio, name='inicio'),
    url(r'^app/portal/general/$', views.inicio_app, name='inicio_app'),
    url(r'^app/portal/detalles/$', views.inicio_app_detalles, name='inicio_app_detalles'),
    url(r'^/data/(?P<agencia>\w+)/$', views.data, name='data'),
    url(r'^app/api/mapAgencias', views.mapAgencias, name='mapAgencias'),
    url(r'^app/api/fusionLines/(?P<agencia>\d+)/(?P<anio>\d+)/$', views.fusionLines, name='fusionLines'),
    url(r'^app/api/fusionCircular/(?P<agencia>\d+)/(?P<asesor>\d+)/(?P<mes>\d+)/$', views.fusionCircular, name='fusionCircular'),
    url(r'^app/api/fusionBarras', views.fusionBarras, name='fusionBarras'),
    #url(r'^about/$', about, name='about'),
    #url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.default.urls')),
]
