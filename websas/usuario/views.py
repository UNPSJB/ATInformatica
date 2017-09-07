from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

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


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('/')