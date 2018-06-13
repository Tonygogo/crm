from django.shortcuts import render

from django.views.decorators.http import require_GET, require_POST
from django.utils import timezone
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.http.response import JsonResponse
from django.core.paginator import Paginator

# Create your views here.
def index(request, template):
    user_str = request.session.get('login_user')
    user = json.loads(user_str, encoding='utf-8')
    return render(request, 'customer_serve_%s.html' % template, {'userName': user.get('userName')})


def create_index(request):
    user_str = request.session.get('login_user')
    user = json.loads(user_str, encoding='utf-8')
    return render(request, 'customer_serve_create.html', {'userName': user.get('userName')})


@require_POST
@csrf_exempt
def add(request):
    # 获取页面参数
    serve = request.POST.dict()
    # 基本参数校验
    # TODO
    # 添加通用字段默认值
    serve['createDate'] = timezone.now()
    serve['updateDate'] = timezone.now()
    serve['isValid'] = 1

    # 保存
    CustomerServe.objects.create(**serve)
    # 返回
    return JsonResponse({'code':1, 'message': '添加成功！'})


# 服务分配
def server_assign(request):
    user_str = request.session.get('login_user')
    user = json.loads(user_str, encoding='utf-8')
    return render(request, 'customer_serve_assign.html', {'userName': user.get('userName')})


# 查询数据
@require_GET
def select_for_page(request):

    select_params = {'createDate': "select DATE_FORMAT(create_date, '%%Y-%%m-%%d %%H:%%i:%%s')",
                     'assignTime': "select DATE_FORMAT(assign_time, '%%Y-%%m-%%d %%H:%%i:%%s')",
                     'serviceProceTime': "select DATE_FORMAT(service_proce_time, '%%Y-%%m-%%d %%H:%%i:%%s')",
                     }
    queryset = CustomerServe.objects.extra(select=select_params)\
                                            .values('id', 'customer', 'overview', 'serveType',  'createPeople',
                                            'createDate', 'state', 'assigner', 'assignTime', 'serviceProce',
                                            'serviceProcePeople', 'serviceProceTime','serviceProceResult',
                                            'serviceRequest', 'myd').order_by('-id').all()

    state = request.GET.get('state')
    if state:
        queryset = queryset.filter(state=state)

    customer = request.GET.get('customer')
    if customer:
        queryset = queryset.filter(customer__icontains=customer)

    overview = request.GET.get('overview')
    if overview:
        queryset = queryset.filter(overview__icontains=overview)

    serve_type = request.GET.get('serveType')
    if serve_type:
        queryset = queryset.filter(serveType=serve_type)

    start_creat_date = request.GET.get('startCreateDate')
    if start_creat_date:
        queryset = queryset.filter(createDate__gte=start_creat_date)

    end_create_date = request.GET.get('endCreateDate')
    if end_create_date:
        queryset = queryset.filter(createDate__lte=end_create_date)

    page = request.GET.get('page', 1)
    page_size = request.GET.get('row', 10)

    # 构建分页对象
    p = Paginator(queryset, page_size)

    # 获取分页后的数据
    data = p.page(page).object_list
    total = p.count

    return JsonResponse({'rows': list(data), 'total': total})


@require_POST
@csrf_exempt
def update(request):
    # 获取参数
    serve = request.POST.dict()
    # 参数校验
    # TODO
    # 获取主键
    pk = serve.pop('id')
    # 填写修改时间
    serve['updateDate'] = timezone.now()
    if '已分配' == serve['state']:
        serve['assignTime'] = timezone.now()
    if '已处理' == serve['state']:
        serve['serviceProceTime'] = timezone.now()
    serve['updateDate'] = timezone.now()
    # 更新
    CustomerServe.objects.filter(pk=pk).update(**serve)
    # 返回
    return JsonResponse({'code':1, 'message': '操作成功'})


def serve_handle(request):
    user_str = request.session.get('login_user')
    user = json.loads(user_str, encoding='utf-8')
    return render(request, 'customer_serve_handle.html', {'userName': user.get('userName')})
