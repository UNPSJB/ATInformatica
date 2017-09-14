from django.views.generic import TemplateView

# Create your views here.
class RubroList(TemplateView):
    template_name = 'rubro/rubros.html'

class RubroCreate(TemplateView):
    template_name = 'rubro/rubro_detail.html'
