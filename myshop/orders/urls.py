from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('orders/', views.orders, name='orders'),
    path('orders/cancelorder/<int:order_id>/', views.cancelorder, name='cancelorder'),
]
