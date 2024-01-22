import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from common.models import Expert, Manager, Session

import secrets
import string


def generate_random_string(length):
    letters = string.ascii_letters
    random_string = ''.join(secrets.choice(letters) for _ in range(length))
    return random_string


# Create your views here.

def get_current(request):
    session_id = request.headers.get("Session-Id")
    session = Session.objects.filter(session_info=session_id)
    if len(session) == 0:
        return JsonResponse({'response': "未登录"})

    session = session[0]
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
    session_id = request.headers.get("Session-Id")
    session = Session.objects.filter(session_info=session_id)
    if len(session) == 0:
        return JsonResponse({'response': "未登录"})

    session = session[0]
    if session.session_status == 0:
        return JsonResponse({'response': "未登录"})
    if session.session_usertype == 'expert':
        return JsonResponse({'response': "非管理员用户"})
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
    # print(username)
    # print(password)
    expert = Expert.objects.filter(expert_name=username, expert_password=password)
    manager = Manager.objects.filter(manager_name=username, manager_password=password)
    if len(expert) > 0:
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = username
            request.session['usertype'] = 'expert'
            session_info = generate_random_string(10)
            exist = Session.objects.filter(session_info=session_info)
            while len(exist) > 0:
                session_info = generate_random_string(10)
                exist = Session.objects.filter(session_info=session_info)
            session = Session(
                session_username=username,
                session_usertype='expert',
                session_last_login_year=datetime.datetime.now().year,
                session_last_login_month=datetime.datetime.now().month,
                session_status=1,
                session_info=session_info,
            )
            session.save()
            res = JsonResponse({'response': '登录成功', 'Session-Id': session.session_info})
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
    elif len(manager) > 0:
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = username
            request.session['usertype'] = 'manager'
            session_info = generate_random_string(10)
            exist = Session.objects.filter(session_info=session_info)
            while len(exist) > 0:
                session_info = generate_random_string(10)
                exist = Session.objects.filter(session_info=session_info)
            session = Session(
                session_username=username,
                session_usertype='manager',
                session_last_login_year=datetime.datetime.now().year,
                session_last_login_month=datetime.datetime.now().month,
                session_status=1,
                session_info=session_info,
            )
            session.save()
            res = JsonResponse({'response': '登录成功', 'Session-Id': session.session_info})
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
    else:
        return JsonResponse({'response': '登陆失败，账号不存在，请先注册'})


def Logout(request):
    session_id = request.headers.get("Session_id")
    session = Session.objects.filter(session_info=session_id)
    if len(session) != 0:
        session = session[0]
        session.session_status = 0
        session.save()
    logout(request)
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
