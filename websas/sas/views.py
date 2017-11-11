from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

class IndexView(TemplateView):
    template_name = 'principal.html'


class SASAdminView(TemplateView):
    template_name = 'el_admin.html'
