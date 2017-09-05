from django.conf.urls import url
from producto import views

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    url(r'^productos$', views.producto, name='producto'),
    url(r'^producto_detail.html', views.producto_detail, name='producto_detail')

]