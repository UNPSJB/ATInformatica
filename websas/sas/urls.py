from django.conf.urls import url
from .views import IndexView
from django.contrib.auth.decorators import login_required
urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.

    # The home page
    url(r'^$', login_required(IndexView.as_view(), login_url='usuario:login'), name='index')
]