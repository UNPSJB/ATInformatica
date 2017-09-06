from django.conf.urls import url
from . import views

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    url(r'^$', views.producto, name='producto'),
    url(r'^producto_detail.html', views.producto_detail, name='producto_detail'),
    url(r'^stock', views.stock, name='stock')

]