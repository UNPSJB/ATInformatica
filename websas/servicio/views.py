from django.views.generic import TemplateView

# Create your views here.
class ServicioCreate(TemplateView):
    template_name = 'servicio/servicio_detail.html'

class ServicioList(TemplateView):
    template_name = 'servicio/servicios.html'