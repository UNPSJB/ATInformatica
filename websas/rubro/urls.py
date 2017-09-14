from django.conf.urls import url
from .views import RubroCreate, RubroList

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
     url(r'^crear/', RubroCreate.as_view(), name="rubro_crear"),
     url(r'^listar/', RubroList.as_view(), name="rubro_listar"),     
]