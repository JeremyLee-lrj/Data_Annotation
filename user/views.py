from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from common.models import Expert, Manager


# Create your views here.

def get_current(request):
    username = request.session.get('username')
    usertype = request.session.get('usertype')
    if username is None:
        return JsonResponse({'response': "未登录"})
    return JsonResponse({'response': "已登录", 'username': username, 'usertype': usertype})


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

    expert = Expert.objects.filter(expert_name=username, expert_password=password)
    manager = Manager.objects.filter(manager_name=username, manager_password=password)
    if expert is not None:
        user = authenticate(username=username, password=password)
        login(request, user)
        request.session['username'] = username
        request.session['usertype'] = 'expert'
        return JsonResponse({'response': '登录成功'})
    elif manager is not None:
        user = authenticate(username=username, password=password)
        login(request, user)
        request.session['username'] = username
        request.session['usertype'] = 'manager'
        return JsonResponse({'response': '登录成功'})
    has_expert_name = Expert.objects.filter(expert_name=username)
    has_manager_name = Manager.objects.filter(manager_name=username)
    if (has_manager_name is not None) and (has_expert_name is not None):
        return JsonResponse({'response': '登陆失败，账号不存在，请先注册'})
    else:
        return JsonResponse({'response': '登陆失败,用户名或密码不正确'})


def Logout(request):
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
