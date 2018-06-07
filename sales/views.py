from django.shortcuts import render
from django.core.paginator import Paginator
from .models import SaleChance
from django.http.response import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.utils import timezone
import json
from django.views.decorators.csrf import csrf_exempt
from crm.common import is_empty

# Create your views here.

# 营销机会管理的首页
def index(request):
    return render(request, "sale_chance.html")


# 分页查询营销机会表
@require_GET
def select_for_page(request):

    # 每页数据大小
    page_size = request.GET.get('rows', 10)
    page = request.GET.get('page', 1)
    # 分页查询：1、构建一个QuerySet 2、构造一个Paginator对象
    # 3、使用Paginator的page()方法进行数据查询，以及count属性获取所有记录
    object_list = SaleChance.objects.extra(select={'createDate': "select DATE_FORMAT(create_date, '%%Y-%%m-%%d %%H:%%i:%%s')"})\
                                    .values('id', 'chanceSource', 'customerId', 'customerName', 'cgjl',
                                     'overview', 'linkMan', 'linkPhone', 'description', 'createMan',
                                     'assignMan', 'assignTime', 'state', 'devResult', 'isValid',
                                     'createDate', 'updateDate').order_by("-id").all()
    # 条件搜索
    customer_name = request.GET.get('customerName')
    if customer_name:
        object_list = object_list.filter(customerName__icontains=customer_name)
    overview = request.GET.get('overview')
    if overview:
        object_list = object_list.filter(overview__icontains=overview)

    create_man = request.GET.get('createMan')

    if create_man:
        object_list = object_list.filter(createMan__icontains=create_man)
    state = request.GET.get('state')
    if state:
        object_list = object_list.filter(state=state)
    p = Paginator(object_list, page_size)
    # 获取每页的数据
    data = p.page(page).object_list
    # 将转化成list进行json输出
    data = list(data)

    # 获取总记录数
    count = p.count
    return JsonResponse({'total': count, 'rows': data})


@require_POST
@csrf_exempt
def save_sale_chance(request):
    # 基本参数校验
    # TODO
    # 保存
    data = request.POST.dict() # 转化成字典
    # 分配状态（分配人）、开发状态、创建、修改日期时间、是否有效、创建人
    data['devResult'] = 0
    data['createDate'] = timezone.now()
    data['updateDate'] = timezone.now()
    data['isValid'] = 1

    # 创建人
    user_str = request.session.get('login_user')
    user = json.loads(user_str, encoding='utf-8')
    data['createMan'] = user.get('userName')

    # 分配状态（分配人）
    assignMan = data.get('assignMan')
    if assignMan:
        data['state'] = 1 # 已分配
        data['assignTime'] = timezone.now()
    else:
        data['state'] = 0 # 未分配
    SaleChance.objects.create(**data)

    return JsonResponse({"code":1, "message":"添加成功！"})


@require_POST
@csrf_exempt
def update_sale_chance(request):
    data = request.POST.dict()  # 转化成字典
    # 基本参数校验
    # TODO
    pk = data.get('id')
    is_empty(pk, message="请选择一条记录进行修改！")
    # 分配状态（分配人）
    assignMan = data.get('assignMan')
    if assignMan:
        data['state'] = 1  # 已分配
        data['assignTime'] = timezone.now()
    else:
        data['state'] = 0  # 未分配
        data['assignTime'] = None
    data['updateDate'] = timezone.now()
    # 修改
    SaleChance.objects.filter(pk=pk).update(**data)
    return JsonResponse({"code": 1, "message": "修改成功！"})


@require_POST
@csrf_exempt
def delete_sale_chances(request):
    ids = request.POST.get('ids')
    # 判断
    is_empty(ids, message="请选择记录进行删除!")

    SaleChance.objects.filter(pk__in=ids.split(',')).update(isValid=0)
    return JsonResponse({"code": 1, "message": "删除成功！"})


