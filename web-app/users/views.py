from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
# Create your views here.

from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User

def index_login(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'account/login.html')
    elif request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=name, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.success(request,"wrong username or password")
            return render(request,'account/login.html')

def index_register(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'account/signup.html')
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        email =  request.POST.get('email')
        if User.objects.filter(username=name).exists():
            messages.success(request, "user exist!")
            return render(request, 'account/signup.html')
        else:
            User.objects.create_user(username=name, password=password, email = email)
        return HttpResponseRedirect('/login/')

def djlogout(request):

    if request.method == 'GET':
        logout(request)
        return HttpResponseRedirect('/login/')
