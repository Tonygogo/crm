from django.shortcuts import render
from .models import *
from django.http.response import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET, require_POST
from crm.common import *
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from random import randint
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


# 查询所有的客户
def find_all(request):
    customers = Customer.objects.values('id', 'name').order_by('-id').all()
    customers = list(customers)
    return JsonResponse(customers, safe=False)


# 列表
def index(request):
    return render(request, 'customer.html')


@require_GET
def select_for_page(request):
    # 每页数据大小
    page_size = request.GET.get('rows', 10)
    page = request.GET.get('page', 1)

    # 查询条件集合：
    select_dict = {'createDate': "select DATE_FORMAT(create_date, '%%Y-%%m-%%d %%H:%%i:%%s')",
                   "updateDate": "select DATE_FORMAT(update_date, '%%Y-%%m-%%d %%H:%%i:%%s')"}
    queryset = Customer.objects.extra(select=select_dict) \
        .values('id', 'khno', 'name', 'area', 'cusManager', 'level',
                'myd', 'xyd', 'address', 'postCode', 'phone',
                'fax', 'website', 'yyzzzch', 'fr', 'zczj',
                'nyye', 'khyh', 'khzh', 'dsdjh', 'gsdjh',
                'state', 'isValid', 'createDate', 'updateDate').order_by("-id").all()

    # 获取查询的条件客户编号和客户名称
    customer_name = request.GET.get('customerName')
    if customer_name:
        queryset = queryset.filter(name__icontains=customer_name)
    customer_no = request.GET.get('customerNo')

    if customer_no:
        queryset = queryset.filter(khno__icontains=customer_no)

    # 构建分页对象
    p = Paginator(queryset, page_size)

    # 获取分页结果
    data = list(p.page(page).object_list)
    total = p.count

    return JsonResponse({'rows': data, 'total': total})


# 添加客户信息
@require_POST
@csrf_exempt
def add(request):
    # 获取参数
    customer = request.POST.dict()
    # 基本的参数校验
    # TODO
    name = customer.get('name')
    is_empty(name, message='请输入客户名称')
    # 验证客户名称是否存在，如果存在就要提示不能重复
    try:
        # 如果存在数据库并且删除过，那么只需要更新删除状态即可
        customer_by_name = Customer.all.get(name=name)
        if customer_by_name.isValid == 0:
            customer['isValid'] = 1
            customer['updateDate'] = timezone.now()
            Customer.all.filter(name=name).update(**customer)
            return JsonResponse({'code':1, 'message': '添加成功！'})
        else:
            return JsonResponse({'code':0, 'message': '该客户已存在，请确认后重试'})
    except ObjectDoesNotExist as e:
        pass
    # 生成客户编号 'KH' + 日期时间 + 三位随机数
    khno = 'KH' + timezone.now().strftime('%Y%m%d%H%M%S') + str(randint(100, 999))
    customer['khno'] = khno
    # 添加创建、修改时间、是否有效
    customer['createDate'] = timezone.now()
    customer['updateDate'] = timezone.now()
    customer['isValid'] = 1
    customer['state'] = 0
    # 加入数据库
    del customer['id']
    Customer.objects.create(**customer)
    return JsonResponse({'code': 1, 'message': '添加成功！'})


# 修改
@require_POST
@csrf_exempt
def update(request):
    # 获取参数
    customer = request.POST.dict()
    # 基本的参数校验
    # TODO
    pk = customer.pop('id')
    is_empty(pk, message='请选择一条记录进行更新')
    name = customer.get('name')
    is_empty(name, message='请输入客户名称')

    # 验证修改后的客户名称是否存在，如果存在就要提示不能重复
    try:
        customer_from_db = Customer.objects.get(pk=pk)
        if customer_from_db.name != name:
            # 进行客户名称的校验
            try:
                customer_by_name = Customer.all.get(name=name)
                return JsonResponse({'code': 0, 'message': '该客户已存在，请确认后重试！'})
            except ObjectDoesNotExist as e:
                pass

        # 添加修改的日期
        customer['updateDate'] = timezone.now()
        Customer.objects.filter(pk=pk).update(**customer)
        return JsonResponse({'code': 1, 'message': '修改成功！'})
    except ObjectDoesNotExist as e:
        return JsonResponse({'code': 0, 'message': '请选择一条记录进行操作！'})


# 删除
@require_POST
@csrf_exempt
def delete(request):
    # # 获取参数
    # ids = request.POST.get('ids')
    # # 校验
    # is_empty(ids)
    # # 执行删除的方法
    # Customer.objects.filter(pk__in=ids.split(',')).update(isValid=0)
    # # 返回
    # return JsonResponse({'code': 1, 'message': '删除成功！'})
    return common_delete(request, Customer)



# 客户联系人页面
def linkman_index(request, customer_id):
    # 查询客户联系人
    customer = Customer.objects.values('id', 'name', 'khno').get(pk=customer_id)
    return render(request, 'linkman.html', customer)


# 分页展示客户联系人
@require_POST
@csrf_exempt
def linkman_select(request, customer_id):
    page_size = request.POST.get('rows', 10)
    page = request.POST.get('page', 1)

    queryset = LinkMan.objects.values('id', 'linkName', 'sex', 'zhiwei', 'officePhone', 'phone')\
        .filter(customer__id=customer_id).order_by('-id')

    p = Paginator(queryset, page_size)

    data = p.page(page).object_list

    return JsonResponse({"total": p.count, 'rows': list(data)})


# 添加客户联系人
@require_POST
@csrf_exempt
def linkman_add(request, customer_id):
    # 获取参数
    linkman = request.POST.dict()
    # TODO 参数校验
    # 校验同一个客户下联系人是否重名
    linkName = linkman.get('linkName')
    try:
        linkman_by_name = LinkMan.objects.get(linkName=linkName, customer__id=customer_id)
        return JsonResponse({'code': 0, 'message': '此联系人已存在！'})
    except ObjectDoesNotExist:
        pass

    # 添加其他默认字段值
    customer = Customer.objects.get(pk=customer_id)
    linkman['customer']=customer
    linkman['createDate'] = timezone.now()
    linkman['updateDate'] = timezone.now()
    linkman['isValid'] = 1
    # 保存
    del linkman['isNewRecord']
    LinkMan.objects.create(**linkman)
    # 返回
    return JsonResponse({'code': 1, 'message': '添加成功！'})


# 修改客户联系人
@require_POST
@csrf_exempt
def linkman_update(request, customer_id):
    # 获取参数
    linkman = request.POST.dict()
    # TODO 参数校验
    pk = linkman.pop('id')
    # 校验联系人是否重名 TODO

    linkman['updateDate'] = timezone.now()

    LinkMan.objects.filter(pk=pk).update(**linkman)
    return JsonResponse({'code': 1, 'message': '更新成功！'})


# 删除客户联系人
@require_POST
@csrf_exempt
def linkman_delete(request, customer_id):
    pk = request.POST.get('id')
    is_empty(pk, message='请选择一条记录进行删除！')
    LinkMan.objects.filter(pk=pk).update(isValid=0, updateDate=timezone.now())
    return JsonResponse({'code': 1, 'message': '删除成功！'})




# 交往记录列表
def contact_index(request, customer_id):
    customer = Customer.objects.values('id', 'name', 'khno').get(pk=customer_id)
    return render(request, 'contact.html', customer)


# 查询客户交往记录
@csrf_exempt
def select_contact(request, customer_id):
    page_size = request.POST.get('rows', 10)
    page = request.POST.get('page', 1)
    select = {'contactTime': "SELECT DATE_FORMAT(contact_time, '%%Y-%%m-%%d %%H:%%i:%%s')"}
    query_set = Contact.objects.extra(select=select)\
                .values('id', 'contactTime', 'address', 'overview') \
                .filter(customer__id=customer_id).order_by('-id')

    p = Paginator(query_set, page_size)
    data = p.page(page).object_list
    data = list(data)
    return JsonResponse({'total': p.count, 'rows': data})


# 添加交往记录
@require_POST
@csrf_exempt
def add_contact(request, customer_id):
    contact = request.POST.dict()
    del contact['isNewRecord']
    customer = Customer.objects.get(pk=customer_id)
    contact['customer'] = customer
    contact['isValid'] = 1
    contact['createDate'] = timezone.now()
    contact['updateDate'] = timezone.now()
    Contact.objects.create(**contact)
    return JsonResponse({'code': 1, 'message': '添加成功！'})


# 修改交往记录
@require_POST
@csrf_exempt
def update_contact(request, customer_id):
    contact = request.POST.dict()
    pk = contact.pop('id')
    contact['updateDate'] = timezone.now()
    Contact.objects.filter(pk=pk).update(**contact)
    return JsonResponse({'code': 1, 'message': '修改成功！'})


# 删除交往记录
@require_POST
@csrf_exempt
def delete_contact(request, customer_id):
    contact = request.POST.dict()
    pk = contact.pop('id')
    contact['updateDate'] = timezone.now()
    contact['isValid'] = 0
    Contact.objects.filter(pk=pk).update(**contact)
    return JsonResponse({'code': 1, 'message': '删除成功！'})


# 历史订单首页
def order_index(request, customer_id):
    customer = Customer.objects.values('id', 'name', 'khno').get(pk=customer_id)
    return render(request, 'customer_orders.html', customer)


# 分页获取数据
@csrf_exempt
def select_customer_order(request, customer_id):
    page_size = request.POST.get('rows', 10)
    page = request.POST.get('page', 1)
    select = {'orderDate': "SELECT DATE_FORMAT(order_date, '%%Y-%%m-%%d %%H:%%i:%%s')"}
    query_set = CustomerOrders.objects.extra(select=select) \
        .values('id', 'orderNo', 'orderDate', 'address', 'state') \
        .filter(customer__id=customer_id).order_by('-id')

    p = Paginator(query_set, page_size)
    data = p.page(page).object_list
    data = list(data)
    return JsonResponse({'total': p.count, 'rows': data})


# 根据订单主键获取订单信息
@csrf_exempt
def find(request, order_id):
    # 获取订单数据
    select = {'orderDate': "SELECT DATE_FORMAT(order_date, '%%Y-%%m-%%d %%H:%%i:%%s')"}
    order = CustomerOrders.objects.extra(select=select) \
        .values('id', 'orderNo', 'orderDate', 'address', 'state', 'totalPrice') \
        .get(pk=order_id)

    return JsonResponse(order)


# 订单订单详情
@csrf_exempt
def order_detail(request, order_id):
    page_size = request.POST.get('rows', 10)
    page = request.POST.get('page', 1)
    query_set = OrdersDetail.objects\
        .values('id', 'goodsName', 'goodsNum', 'unit', 'price', 'sum') \
        .filter(order__id=order_id).order_by('-id')

    p = Paginator(query_set, page_size)
    data = p.page(page).object_list
    data = list(data)
    return JsonResponse({'total': p.count, 'rows': data})


# 客户流失主页
def loss_index(request):
    return render(request, "loss_index.html")



# 分页查询客户流失列表
@require_GET
def customer_loss_query(request):
    page_size = request.GET.get('rows', 10)
    page = request.GET.get('page', 1)
    select = {'lastOrderTime': "SELECT DATE_FORMAT(last_order_time, '%%Y-%%m-%%d %%H:%%i:%%s')",
              'confirmLossTime': "SELECT DATE_FORMAT(confirm_loss_time, '%%Y-%%m-%%d %%H:%%i:%%s')"
              }
    queryset = CustomerLoss.objects.extra(select=select).values('id', 'cusNo', 'cusName', 'cusManager',
                                           'lastOrderTime', 'confirmLossTime',
                                           'state', 'lossReason').order_by("-id").all()

    # 构建搜索条件
    cus_name = request.GET.get('cusName')
    if cus_name:
        queryset = queryset.filter(cusName__icontains=cus_name)
    cus_manager = request.GET.get('cusManager')
    if cus_manager:
        queryset = queryset.filter(cusManager__icontains=cus_manager)
    state = request.GET.get('state')
    if state:
        queryset = queryset.filter(state=state)

    # 构建分页对象
    p = Paginator(queryset, page_size)

    # 获取数据
    data = p.page(page).object_list
    total = p.count

    # 返回数据
    return JsonResponse({'rows': list(data), 'total': total})


# 客户流失暂缓主页
def reprieve_index(request, loss_id):
    # 先查询流失的信息
    select = {'lastOrderTime': "SELECT DATE_FORMAT(last_order_time, '%%Y-%%m-%%d %%H:%%i:%%s')"
              }
    loss = CustomerLoss.objects.extra(select=select).values('id', 'cusNo',  'cusName', 'cusManager',
                                           'lastOrderTime').get(pk=loss_id)
    # 跳转到模板
    return render(request, 'reprieve_index.html', loss)


# 查询流失客户下的暂缓措施
@csrf_exempt
def select_reprieve(request, loss_id):
    data = CustomerReprieve.objects.values('id', 'measure')\
        .filter(customerLoss__id=loss_id).order_by('-id').all()
    return JsonResponse(list(data), safe=False)


# 添加暂缓措施
@csrf_exempt
@require_POST
def add_reprieve(request, loss_id):
    # 获取参数
    measure = request.POST.get('measure')
    is_empty(measure, message="请输入暂缓的措施！")
    reprieve = dict()
    loss = CustomerLoss.objects.get(pk=loss_id)
    reprieve['customerLoss'] = loss
    reprieve['measure'] = measure
    reprieve['createDate'] = timezone.now()
    reprieve['updateDate'] = timezone.now()
    reprieve['isValid'] = 1

    # 保存
    obj = CustomerReprieve.objects.create(**reprieve)
    result = {'id':obj.id, 'measure':obj.measure}
    return JsonResponse(result)


# 修改暂缓措施
@csrf_exempt
@require_POST
def update_reprieve(request, loss_id):
    measure = request.POST.get('measure')
    pk = request.POST.get('id')
    reprieve = dict()
    reprieve['measure'] = measure
    reprieve['updateDate'] = timezone.now()
    CustomerReprieve.objects.filter(pk=pk).update(**reprieve)
    # return JsonResponse({'code': 1, 'message': '修改成功！'})
    return JsonResponse(request.POST.dict())


# 删除暂缓措施
@csrf_exempt
@require_POST
def delete_reprieve(request, loss_id):
    pk = request.POST.get('id')
    CustomerReprieve.objects.filter(pk=pk).update(isValid=0, updateDate=timezone.now())
    return JsonResponse({'code': 1, 'message': '删除成功！'})



# 确认流失
@csrf_exempt
@require_POST
def confirm_loss(request, loss_id):
    loss_reason = request.POST.get('lossReason')
    is_empty(loss_reason, message='请输入流失原因')
    # 更新t_customer_loss表流失原因以及确认流失状态
    loss = CustomerLoss.objects.get(pk=loss_id)
    loss.lossReason = loss_reason
    loss.state = 1
    loss.updateDate = timezone.now()
    loss.confirmLossTime = timezone.now()
    loss.save()
    # CustomerLoss.objects.filter(pk=loss_id).update(lossReason=loss_reason, state=1)
    # 更新t_customer表状态为确认流失状态
    # loss = CustomerLoss.objects.get(pk=loss_id)
    Customer.objects.filter(khno=loss.cusNo).update(state=2)
    return JsonResponse({'code': 1, 'message': '操作成功！'})


