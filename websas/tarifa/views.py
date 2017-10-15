from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
# Create your views here.

class TarifaCreate(View):
    # username = request.GET.get('username', None)
    # data = {
    #     'is_taken': User.objects.filter(username__iexact=username).exists()
    # }
    # if data['is_taken']:
    #     data['error_message'] = 'A user with this username already exists.'
    def post(self, request, *args, **kwargs):
        print(request.POST.get("tarea"))
        print(request.POST.get("tipo_servicio"))
        print(request.POST.get("precio"))
        
        data = {
            "coso": "coseno"
        }
        return JsonResponse(data)