from django.shortcuts import render
from .models import *
from django.http.response import JsonResponse
# Create your views here.

def datadic_list(request):
    # SELECT * from t_datadic WHERE data_dic_name='客户等级';
    datas = DataDic.objects.values('id', 'dataDicName', 'dataDicValue')\
        .filter(dataDicName='客户等级').order_by('-id').all()
    return JsonResponse(list(datas), safe=False)


