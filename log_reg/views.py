from django.shortcuts import render
from django.template.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from log_reg.models import userdata
from django.contrib import messages
def login(request):
    c={}
    c.update(csrf(request))
    return render(request,'login4.html',c)
def register(request):
    c={}
    c.update(csrf(request))
    return render(request,'register.html',c)
def auth_register(request):
    username=request.POST.get('Username');
    name=request.POST.get('Name')
    passw=request.POST.get('password')
    mob=request.POST.get('Mob')
    try:
        User.objects.create(username=username,first_name=name)
        u=User.objects.get(username=username)
        u.set_password(passw)
        u.save()
        userdata.objects.create(username=u,mob=mob)
        messages.info(request,'You are Registered Now. Login to Continue')
        return HttpResponseRedirect('/log/login/')
    except:
        messages.error(request,'Username already exists')
        return HttpResponseRedirect('/log/register/')
def auth_my_user(request):
    name=request.POST.get('Name')
    passw=request.POST.get('password')
    user=auth.authenticate(username=name,password=passw)
    print(user)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/chat/home')
    else:
        try:
            User.objects.get(username=name)
            messages.error(request,'Invalid Password')
            return HttpResponseRedirect('/log/login')
        except:
            messages.error(request,'Invalid User')
            return HttpResponseRedirect('/log/login/')
def logout(request):
    auth.logout(request)
    messages.info(request,'Thankyou For Using')
    return HttpResponseRedirect('/log/login/')
    