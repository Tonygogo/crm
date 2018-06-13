from django.urls import path
from . import views

app_name = 'customer'
urlpatterns = [
    path('<int:loss_id>/confirm_loss/', views.confirm_loss, name='confirm_loss'),
    path('<int:loss_id>/delete_reprieve/', views.delete_reprieve, name='delete_reprieve'),
    path('<int:loss_id>/update_reprieve/', views.update_reprieve, name='update_reprieve'),
    path('<int:loss_id>/add_reprieve/', views.add_reprieve, name='add_reprieve'),
    path('<int:loss_id>/select_reprieve/', views.select_reprieve, name='select_reprieve'),
    path('<int:loss_id>/reprieve_index/', views.reprieve_index, name='reprieve_index'),
    path('customer_loss_query/', views.customer_loss_query, name='customer_loss_query'),
    path('loss_index/', views.loss_index, name='loss_index'),



    path('<int:order_id>/order_detail/', views.order_detail, name='order_detail'),
    path('<int:order_id>/find/', views.find, name='find'),
    path('<int:customer_id>/select_customer_order/', views.select_customer_order, name='select_customer_order'),
    path('<int:customer_id>/order_index/', views.order_index, name='order_index'),

    path('<int:customer_id>/delete_contact/', views.delete_contact, name='delete_contact'),
    path('<int:customer_id>/update_contact/', views.update_contact, name='update_contact'),
    path('<int:customer_id>/add_contact/', views.add_contact, name='add_contact'),
    path('<int:customer_id>/select_contact/', views.select_contact, name='select_contact'),
    path('<int:customer_id>/contact_index/', views.contact_index, name='contact_index'),


    path('<int:customer_id>/linkman_delete/', views.linkman_delete, name='linkman_delete'),
    path('<int:customer_id>/linkman_update/', views.linkman_update, name='linkman_update'),
    path('<int:customer_id>/linkman_add/', views.linkman_add, name='linkman_add'),
    path('<int:customer_id>/linkman_select/', views.linkman_select, name='linkman_select'),
    path('<int:customer_id>/linkman_index/', views.linkman_index, name='linkman_index'),


    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('add/', views.add, name='add'),
    path('select_for_page/', views.select_for_page, name='select_for_page'),
    path('index/', views.index, name='index'),
    path('find_all/', views.find_all, name='find_all'),
]