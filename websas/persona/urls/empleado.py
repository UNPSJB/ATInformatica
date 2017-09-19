from django.contrib.auth.decorators import login_required
from django.conf.urls import url, include

urlpatterns = [
    url(r'^tecnico/', include('persona.urls.tecnico', namespace="tecnico")),
    url(r'^jefe/', include('persona.urls.jefe_taller', namespace="jefe")),
    url(r'^gerente/', include('persona.urls.gerente', namespace="gerente")),
]