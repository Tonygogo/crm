from django.urls import path
from . import views

app_name = 'system'
urlpatterns = [
    path('find_customer_manager/', views.find_customer_manager, name='find_customer_manager'),
    path('update_password/', views.update_password, name='update_password'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]