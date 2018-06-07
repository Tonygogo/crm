from django.urls import path
from . import views

app_name = 'customer'
urlpatterns = [
    path('find_all/', views.find_all, name='find_all'),
]