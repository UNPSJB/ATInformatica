from django.conf.urls import url
from .views import ServicioCreate, ServicioList 

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    url(r'^crear/', ServicioCreate.as_view(), name="servicio_crear"),
    url(r'^servicio/', ServicioList.as_view(), name="servicio_listar"),
]
