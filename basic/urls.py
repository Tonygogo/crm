from django.urls import path
from . import views

app_name = 'basic'
urlpatterns = [

    path('datadic_list/', views.datadic_list, name='datadic_list'),
]