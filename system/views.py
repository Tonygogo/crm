from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http.response import JsonResponse
from .models import User
from hashlib import md5
from django.core.exceptions import ObjectDoesNotExist
import json
from crm.common import ParamException, is_empty
# Create your views here.


@require_POST
def login(request):
    # 获取参数
    username = request.POST.get('username')
    password = request.POST.get('password')
    # 非空验证
    is_empty(username, message='请输入账号')
    is_empty(password, message='请输入密码！')
    # 如果用户已登录，不需要登录
    user_str = request.session.get('login_user')
    is_empty(user_str, code=2, message='用户已登录！')

    # 先将password进行md5加密
    md = md5(password.encode(encoding='utf-8'))
    password_md5 = md.hexdigest()
    try:
        user = User.objects.values('id', 'userName', 'trueName', 'phone',
                                   'email').get(userName=username, password=password_md5)
        # 保持登录状态
        request.session['login_user'] = json.dumps(user)
        return JsonResponse({'code': 1, 'message': '登录成功！'})
    except ObjectDoesNotExist as e:
        raise ParamException(message='用户或密码失败！')
        # return JsonResponse({'code': 0, 'message': '用户或密码失败！'})


@require_POST
def update_password(request):
    # a) 是否用户处于登录状态
    user_str = request.session.get('login_user')
    is_empty(user_str, message= '请登录')

    # b) 非空校验，新密码和确认密码也要校验
    old_password = request.POST.get('old_password')
    is_empty(old_password, message='请输入原密码')
    new_password = request.POST.get('new_password')
    is_empty(new_password, message='请输入新密码')
    confirm_new_password = request.POST.get('confirm_new_password')
    is_empty(confirm_new_password, message='请输入确认新密码')
    if new_password != confirm_new_password:
        raise ParamException.create_error('两次密码输入不相等')


    # c) 原密码是否正确，就是将原密码(加密)  和数据库中的密码进行对比
    user = json.loads(user_str, encoding='utf-8')
    user_obj = User.objects.get(pk=user.get('id'))
    password = user_obj.password
    md = md5(old_password.encode(encoding='utf-8'))
    old_password = md.hexdigest()
    if password != old_password:
        return JsonResponse({'code': 0, 'message': '原密码输入不正确，请重新输入'})
    # d) 修改密码
    user_obj.password = md5(new_password.encode(encoding='utf-8')).hexdigest()
    user_obj.save()
    # e) 返回结果
    return JsonResponse({'code': 1, 'message': '修改成功！'})


def logout(request):
    request.session.flush()
    return redirect('index:index')
