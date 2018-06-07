from django.shortcuts import render
from .models import Customer
from django.http.response import JsonResponse
# Create your views here.


# 查询所有的客户
def find_all(request):
    customers = Customer.objects.values('id', 'name').order_by('-id').all()
    customers = list(customers)
    return JsonResponse(customers, safe=False)
