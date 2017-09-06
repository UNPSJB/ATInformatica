"""gentella URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # app/ -> Genetelella UI and resources
    url(r'^', include('sas.urls')),
    url(r'^develop/', include('lela.urls')),
    url(r'^producto/', include('producto.urls')),
    url(r'^persona/', include('persona.urls')),
    url(r'^rubro/', include('rubro.urls')),
    url(r'^servicio/', include('servicio.urls')),
    url(r'^usuario/', include('usuario.urls')),
    url(r'accounts/login/$', views.login, name='login'),
    url(r'accounts/logout/$', views.logout, name='logout', kwargs={'next_page': '/'}),

]
