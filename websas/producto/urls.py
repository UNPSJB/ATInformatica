from django.conf.urls import url
from .views import ProductoCreate, ProductoList 

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    url(r'^crear$', ProductoCreate.as_view(), name="producto_crear"),
    url(r'^listar$', ProductoList.as_view(), name="producto_listar"),
]