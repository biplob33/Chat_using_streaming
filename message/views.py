from django.shortcuts import   render
from django.contrib import auth
from django.http.response import HttpResponseRedirect, JsonResponse
from django.http import StreamingHttpResponse
from message.models import message,unreadmessage
from django.contrib.auth.models import User
from django.template.context_processors import csrf
from log_reg.models import userdata
from django.utils.timezone import now
import datetime
import time
import concurrent.futures
from django.contrib import messages as html_message
def main_page(request):
    return render(request,'home_page.html')
def is_online(user,to):
    u=userdata.objects.get(username=User.objects.get(username=str(to)))
    if u.online==False:
        a=False
    else:
        real = now()
        user_time = u.last_active
        x=real-user_time
        if (datetime.timedelta(0,2))<x:
            u.online = False
            a=False
            u.save()
        else:
            a=True
    return a
def make_online(username):
    u=userdata.objects.get(username=username)
    u.last_active=now()
    u.online=True
    u.save()
def chat_home(request):
    username=auth.get_user(request)
    encpy=request.GET['to']
    u=userdata.objects.get(encpy=encpy)
    to=str(u.username)
    if str(username) == 'AnonymousUser':
        html_message.error(request,'Please login to Continue.')
        return HttpResponseRedirect('/log/login/')
    m=message.objects.all()
    con={'chat':m,'username':str(username),'to':str(to)}
    con.update(csrf(request))
    return render(request,'chat.html',con)
def frn(request):
    username=auth.get_user(request)
    if str(username) == 'AnonymousUser':
        html_message.error(request,'Please login to Continue.')
        return HttpResponseRedirect('/log/login/')
    p=userdata.objects.all()
    
    username=auth.get_user(request)
    make_online(username)
    for i in p:
        if i.online:
            is_online(username, i)
    con={'user':username,'data':p,}
    return render(request,'home.html',con)
def post(request):
    user=auth.get_user(request)
    msg=request.POST.get('msgbox',None)
    to=request.POST.get('to')
    c=message(sender=str(user),to=str(to),message_data=msg)
    u=userdata.objects.get(username=User.objects.get(username=to))
    if msg!='' and msg is not None:
        c.save()
        if not u.online:
            unreadmessage.objects.create(mess_id=c.id)
    return JsonResponse({ 'msg': msg, 'user': str(user) })


def get_messages(request):
    print('getting Called')
    username=auth.get_user(request)
    to=request.GET.get('to')
    make_online(username)
    
    count=request.GET.get('count')
    
    initial_msg = {}
    while True:
        a=is_online(username, to)
        x=message.objects.filter(sender=to,to=username)
        real_count=len(x)
        out = {}
        if int(count)==real_count:
            out = {'data':False,'online':a}
        else:
            msg=[]
            for i in range((real_count-int(count))):
                curr=x[real_count-i-1]
                
                msg.append(str(curr))
            out = {'data':True,'msg':msg,'online':a,}
            if initial_msg != out:
                initial_msg = out.copy()
                count = real_count
                #yield 'data:' + json.dumps(out) + '\n\n' 
                #time.sleep(1)
                return out
        time.sleep(0.3)
def messages(request):

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(get_messages, request)
        return_value = future.result()

    
        
    response = JsonResponse(return_value)
    response['Content-Type'] = 'text/event-stream'
    response['Cache-Control'] = 'no-cache',
    #response['Connection']=  'keep-alive'

    return response