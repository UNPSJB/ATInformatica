from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import Usuario
from persona.models import Persona
from django.views.generic import View

class RegistrarUsuario(View):

    def get(self, request, *args, **kwargs):
        # import ipdb;ipdb.set_trace()
        pk = self.kwargs.get('pk', 0)
        persona = Persona.objects.get(pk=pk)
        user = Usuario.objects.create_user(username=persona.doc,password=persona.doc, persona = persona)
        user.save()
        return HttpResponseRedirect('cliente:cliente_listar')
"""
def registrarUsuario(request, pk):
    #import ipdb 
    #ipdb.set_trace()
    if request.method == 'GET':
        user = Usuario.objects.create_user(username='otroPirullo', password='pirulo1234', persona = Persona.objects.get(pk=pk))
        user.save()
        return redirect('/')
    else: 
        return render(request, 'login.html')
"""
@csrf_protect
def login_user(request):
    if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else: 
        return render(request, 'login.html')


@login_required(login_url='usuario:login')
def logout_user(request):
    logout(request)
    return redirect('/')