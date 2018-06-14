from django.urls import path
from . import views

app_name = 'report'
urlpatterns = [
    path('customer_loss_index/', views.customer_loss_index, name='customer_loss_index'),

    path('customer_serve/', views.customer_serve, name='customer_serve'),
    path('customer_serve_index/', views.customer_serve_index, name='customer_serve_index'),

    path('customer_component/', views.customer_component, name='customer_component'),
    path('customer_component_index/', views.customer_component_index, name='customer_component_index'),

    path('customer_contribute/', views.customer_contribute, name='customer_contribute'),
    path('customer_contribute_index/', views.customer_contribute_index, name='customer_contribute_index'),
]