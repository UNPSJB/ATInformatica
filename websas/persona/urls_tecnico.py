from django.conf.urls import url
from . import views

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.

    # The home page
    url(r'^$', views.tecnico, name='tecnico'),
    url(r'^(?P<pk>\d+)$', views.tecnico_detail, name='tecnico_detail')
]