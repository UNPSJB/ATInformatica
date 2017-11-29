from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import Reportes
urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.

    url(r'^ver/', login_required(Reportes.as_view(), login_url='usuario:login'), name="reportes"),
]
