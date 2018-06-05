from django.shortcuts import render, redirect
from hashlib import md5
import json
# Create your views here.


def index(request):
    # 如果登录，就直接跳转到登录后的页面
    user_str = request.session.get('login_user')
    if user_str:
        return redirect("index:main")
    return render(request, 'index.html')


def main(request):
    # 获取登录的用户名
    user_str = request.session.get('login_user')
    if user_str is None:
        return redirect('index:index')
    user = json.loads(user_str, encoding='utf-8')
    return render(request, 'main.html', user)
