from django.views.generic import TemplateView, View
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

class IndexView(TemplateView):
    template_name = 'principal.html'


class ConfigView(View):
    def post(self, request):
        request.session['lela_estilo'] = (request.POST['lela_estilo'] == 'true')
        return HttpResponse(status=200)


class SASAdminView(TemplateView):
    template_name = 'el_admin.html'
