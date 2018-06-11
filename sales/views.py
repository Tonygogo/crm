from django.shortcuts import render
from django.core.paginator import Paginator
from .models import SaleChance, CusDevPlan
from django.http.response import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.utils import timezone
import json
from django.views.decorators.csrf import csrf_exempt
from crm.common import *
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
    select_params = {'createDate': "select DATE_FORMAT(create_date, '%%Y-%%m-%%d %%H:%%i:%%s')",
                     'assignTime': "select DATE_FORMAT(assign_time, '%%Y-%%m-%%d %%H:%%i:%%s')"}
    object_list = SaleChance.objects.extra(select=select_params)\
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

    dev_result = request.GET.get('devResult')
    if dev_result:
        object_list = object_list.filter(devResult=dev_result)

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
    # ids = request.POST.get('ids')
    # # 判断
    # is_empty(ids, message="请选择记录进行删除!")
    #
    # SaleChance.objects.filter(pk__in=ids.split(',')).update(isValid=0)
    # return JsonResponse({"code": 1, "message": "删除成功！"})
    return common_delete()

def plan_index(request):
    return render(request, "plan_index.html")


def cus_dev_index(request, sale_chance_id):
    show = request.GET.get('show')
    # 读取营销机会信息 -- 使用get方式获取数据，不存在会报异常 ObjetDoesnotExist
    sale_chance = SaleChance.objects.get(pk=sale_chance_id)
    return render(request, "cus_dev_plan.html", {"sale_chance":sale_chance, 'show':show})


# 获取营销机会下的所有计划开发项
@csrf_exempt
def cus_dev_list(request, sale_chance_id):

    cus_dev_plans = CusDevPlan.objects.extra(select={'planDate': 'date_format(plan_date, "%%Y-%%m-%%d")'})\
        .values('id', 'planItem', 'planDate', 'exeAffect').filter(saleChance__id=sale_chance_id)
    cus_dev_plans = list(cus_dev_plans)
    return JsonResponse(cus_dev_plans, safe=False)


@csrf_exempt
@require_POST
def cus_dev_add(request, sale_chance_id):
    # 基本参数校验
    # TODO
    data = request.POST.dict()
    # 删除isNewRecord这个值
    del data['isNewRecord']
    # 获取营销机会对象
    sale_chance = SaleChance.objects.get(pk=sale_chance_id)
    data['saleChance'] = sale_chance
    data['isValid'] = 1
    data['createDate'] = timezone.now()
    data['updateDate'] = timezone.now()
    CusDevPlan.objects.create(**data)

    # 要更新营销机会的开发状态为开发中
    if sale_chance.devResult != 1:
        SaleChance.filter(pk=sale_chance_id).update(devResult=1)

    return JsonResponse({'code':1, 'message':'添加成功'})

@csrf_exempt
@require_POST
def cus_dev_delete(request, sale_chance_id):
    pk = request.POST.get('id')
    CusDevPlan.objects.filter(pk=pk).update(isValid=0, updateDate=timezone.now())
    return JsonResponse({'code':1, 'message':'删除成功'})


@csrf_exempt
@require_POST
def cus_dev_update(request, sale_chance_id):
    data = request.POST.dict()
    pk = data.pop('id')
    data['updateDate'] = timezone.now()
    CusDevPlan.objects.filter(pk=pk).update(**data)
    return JsonResponse({'code': 1, 'message': '修改成功'})


@csrf_exempt
@require_POST
def update_dev_result(request, sale_chance_id):
    dev_result = request.POST.get('devResult')
    SaleChance.objects.filter(pk=sale_chance_id).update(devResult=dev_result, updateDate=timezone.now())
    return JsonResponse({'code': 1, 'message': '操作成功'})
