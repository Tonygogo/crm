from django.urls import path
from . import views

app_name = 'sales'
urlpatterns = [
    path('delete_sale_chances/', views.delete_sale_chances, name='delete_sale_chances'),
    path('update_sale_chance/', views.update_sale_chance, name='update_sale_chance'),
    path('save_sale_chance/', views.save_sale_chance, name='save_sale_chance'),
    path('select_for_page/', views.select_for_page, name='select_for_page'),
    path('index/', views.index, name='index'),
]