from django.urls import path
from . import views

app_name = 'serve'
urlpatterns = [
    path('update/', views.update, name='update'),
    path('select_for_page/', views.select_for_page, name='select_for_page'),
    path('server_assign/', views.server_assign, name='server_assign'),
    path('add/', views.add, name='add'),
    path('create_index/', views.create_index, name='create_index'),
    path('index/<str:template>/', views.index, name='index'),
]