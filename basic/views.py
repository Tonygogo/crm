from django.shortcuts import render
from .models import *
from django.http.response import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
# Create your views here.

def datadic_list(request):
    # SELECT * from t_datadic WHERE data_dic_name='客户等级';
    data_dic_name = request.GET.get('dataDicName', '客户等级')
    datas = DataDic.objects.values('id', 'dataDicName', 'dataDicValue')\
        .filter(dataDicName=data_dic_name).order_by('-id').all()
    return JsonResponse(list(datas), safe=False)


# 跳转到模板
def datadic_index(request):
    return render(request, 'datadic_index.html')


# 分页查询数据
@require_GET
def select_datadic(request):
    # 查询的命令
    queryset = DataDic.objects.values('id', 'dataDicName', 'dataDicValue').order_by('-id').all()
    name = request.GET.get('dataDicName')
    if name:
        queryset = queryset.filter(dataDicName__icontains=name)
    value = request.GET.get('dataDicValue')
    if value:
        queryset = queryset.filter(dataDicValue__icontains=value)
    # 获取分页的参数 page page_size
    page = request.GET.get('page', 1)
    page_size = request.GET.get('rows', 10)
    # 构建分页对象
    p = Paginator(queryset, page_size) # 传入结果集以及每页多少条
    # 分页查询结果集
    rows = p.page(page).object_list
    # 返回数据
    return JsonResponse({'rows': list(rows), 'total': p.count})


@require_GET
def find_all(request):
    # SELECT * from t_datadic where is_valid=1
    datas = DataDic.objects.values('dataDicName').distinct().all()
    return JsonResponse(list(datas), safe=False)


# 添加数据
@require_POST
@csrf_exempt
def add_datadic(request):
    # 获取参数
    datadic = request.POST.dict()
    # 基本参数校验
    # TODO

    # 唯一性校验
    # TODO
    # 添加默认字段值
    datadic['isValid'] = 1
    datadic['createDate'] = timezone.now()
    datadic['updateDate'] = timezone.now()
    # 添加数据
    DataDic.objects.create(**datadic)
    return JsonResponse({'code': 1, 'message': '添加成功！'})


# 字典修改
@require_POST
@csrf_exempt
def update_datadic(request):
    data_dic = request.POST.dict()
    pk = data_dic.pop('id')
    # 基本参数校验
    # 唯一性校验
    # TODO
    data_dic['updateDate'] = timezone.now()
    DataDic.objects.filter(pk=pk).update(**data_dic)
    return JsonResponse({'code': 1, 'message': '修改成功！'})


# 字典删除
@require_POST
@csrf_exempt
def delete_datadic(request):
    ids = request.POST.get('ids')
    DataDic.objects.filter(pk__in=ids.split(',')).update(isValid=0, updateDate=timezone.now())
    return JsonResponse({'code': 1, 'message': '删除成功！'})


# 产品首页
def product_index(request):
    return render(request, 'product_index.html')

# 分页查询产品数据
@require_GET
def select_product(request):

    # 分页参数
    page = request.GET.get('page')
    page_size = request.GET.get('rows')
    # 分页数据集合
    queryset = Product.objects.values('id', 'productName', 'model',
                                      'unit', 'price', 'store', 'remark').order_by('-id').all()
    product_name = request.GET.get('productName')
    if product_name:
        queryset = queryset.filter(productName__icontains=product_name)

    # 分页对象
    p = Paginator(queryset, page_size)
    # 分页结果
    total = p.count
    rows = list(p.page(page).object_list)
    # 返回
    return JsonResponse({'rows': rows, 'total': total})