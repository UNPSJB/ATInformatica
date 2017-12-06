from django.views.generic import TemplateView, View
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required


class AjaxFormView(View):
    """ Vista para manejar las peticiones con ajax a traves de un formulario
    Las vistas que tengan que manejar este tipo de peticiones tienen que heredar
    de AjaxFormView y redefinir el metodo 'form_class' por el formulario correspondiente
    que se desee utilizar. Tambien se pueden redefinir los mensajes que se devuelven en el JsonResponse
    tanto para el caso de exito como el de error, y el codigo de error devuelto"""
    form_class = None
    response_success_data = "success"
    response_error_data = "error"
    response_error_status_code = 403

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST or None)

        if form.is_valid():
            form.save()
            return JsonResponse({"data": self.response_success_data})

        response = JsonResponse({"data": self.response_error_data})
        response.status_code = self.response_error_status_code
        return response


class IndexView(TemplateView):
    template_name = 'principal.html'


class SASAdminView(TemplateView):
    template_name = 'el_admin.html'

