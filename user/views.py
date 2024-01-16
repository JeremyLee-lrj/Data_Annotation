import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from common.models import Expert, Manager, Session


# Create your views here.

def get_current(request):
    if len(Session.objects.all()) == 0:
        Session.objects.create(
            session_username="-",
            session_usertype="-",
            session_status=0
        )
    else:
        session = Session.objects.all()[0]
        now = datetime.datetime.now()
        if now.year != session.session_last_login_year or now.month != session.session_last_login_month:
            session.session_status = 0

    session = Session.objects.all()[0]
    if session.session_status == 0:
        return JsonResponse({'response': "未登录"})
    else:
        return JsonResponse(
            {
                'response': "已登录",
                'username': session.session_username,
                'usertype': session.session_usertype
            }
        )
    # username = request.session.get('username')
    # usertype = request.session.get('usertype')
    # if username is None:
    #     res = JsonResponse({'response': "未登录"})
    # else:
    #     res = JsonResponse({'response': "已登录", 'username': username, 'usertype': usertype})
    # res['Access-Control-Allow-Origin'] = request.get_host()
    # res['Same-Site'] = 'None'
    # res['Secure'] = True
    # # print(res.headers)
    # # res['Set-Cookie'] = res['Set-Cookie'] + '; SameSite=None; Secure'
    # res['Session-Cookie-Same-Site'] = 'None'
    # res['Session-Cookie-Secure'] = True
    # res['Session-Cookie-HttpOnly'] = False
    # res['Referrer-Policy'] = 'no-referrer'
    # res['Access-Control-Allow-Credentials'] = 'true'
    # res['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
    # res['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    # return res


def List(request):
    qs = Expert.objects.all()
    res = []
    for expert in qs:
        data = {'expert_id': expert.expert_id, 'expert_name': expert.expert_name,
                'expert_area': expert.expert_area}
        res.append(data)

    return JsonResponse({"response": res})


def Login(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    if len(Session.objects.all()) == 0:
        Session.objects.create(
            session_username="-",
            session_usertype="-",
            session_status=0
        )
    session = Session.objects.all()[0]
    expert = Expert.objects.filter(expert_name=username, expert_password=password)
    manager = Manager.objects.filter(manager_name=username, manager_password=password)
    if len(expert) > 0:
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = username
            request.session['usertype'] = 'expert'
            session.session_username = username
            session.session_usertype = 'expert'
            session.session_last_login_year = datetime.datetime.now().year
            session.session_last_login_month = datetime.datetime.now().month
            session.session_status = 1
            session.save()
            res = JsonResponse({'response': '登录成功'})
            # res['Access-Control-Allow-Origin'] = request.get_host()
            # res['Same-Site'] = 'None'
            # res['Secure'] = True
            # # print(res['Set-Cookie'])
            # # res['Set-Cookie'] = res['Set-Cookie'] + '; SameSite=None; Secure'
            # res['Session-Cookie-Same-Site'] = 'None'
            # res['Session-Cookie-Secure'] = True
            # res['Session-Cookie-HttpOnly'] = False
            # res['Referrer-Policy'] = 'no-referrer'
            # res['Access-Control-Allow-Credentials'] = 'true'
            # res['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
            # res['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            return res
        else:
            return JsonResponse({'response': '登陆失败,用户名或密码不正确'})
    elif len(manager) > 0:
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = username
            request.session['usertype'] = 'manager'
            session.session_username = username
            session.session_usertype = 'manager'
            session.session_last_login_year = datetime.datetime.now().year
            session.session_last_login_month = datetime.datetime.now().month
            session.session_status = 1
            session.save()
            res = JsonResponse({'response': '登录成功'})
            res['Access-Control-Allow-Origin'] = request.get_host()
            res['Same-Site'] = 'None'
            res['Secure'] = True
            # print(res['Set-Cookie'])
            # res['Set-Cookie'] = res['Set-Cookie'] + '; SameSite=None; Secure'
            res['Session-Cookie-Same-Site'] = 'None'
            res['Session-Cookie-Secure'] = True
            res['Session-Cookie-HttpOnly'] = False
            res['Referrer-Policy'] = 'no-referrer'
            res['Access-Control-Allow-Credentials'] = 'true'
            res['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
            res['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            return res
        else:
            return JsonResponse({'response': '登陆失败,用户名或密码不正确'})
    else:
        return JsonResponse({'response': '登陆失败，账号不存在，请先注册'})


def Logout(request):
    if len(Session.objects.all()) == 0:
        Session.objects.create(
            session_username="-",
            session_usertype="-",
            session_status=0
        )
    logout(request)
    session = Session.objects.all()[0]
    session.session_status = 0
    session.save()
    return JsonResponse({'response': '登出成功'})


def Register(request):
    expert_name = request.POST.get('username')
    expert_area = request.POST.get('user_area')
    expert_password = request.POST.get('password')
    res = Expert.objects.filter(expert_name=expert_name)
    if len(res) != 0:
        return JsonResponse({'response': '注册失败，用户名已存在'})
    User.objects.create_user(username=expert_name, password=expert_password)
    Expert.objects.create(expert_name=expert_name, expert_password=expert_password,
                          expert_area=expert_area)
    return JsonResponse({'response': '注册成功'})


def Register_Manager(request):
    manager_name = request.POST.get('username')
    manager_password = request.POST.get('password')
    res = Manager.objects.filter(manager_name=manager_name)
    if len(res) != 0:
        return JsonResponse({'response': '注册失败，用户名已存在'})
    User.objects.create_user(username=manager_name, password=manager_password)
    Manager.objects.create(manager_name=manager_name, manager_password=manager_password)
    return JsonResponse({'response': '注册成功'})
