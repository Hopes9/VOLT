from django.urls import path

from .views import Post_order, My_orders, Create_pay, Cdek_order

urlpatterns = [
    path("buy/", Post_order.as_view()),
    path("my_orders/", My_orders.as_view()),
    path("pay_order/", Create_pay.as_view()),
    path("cdek_order/", Cdek_order.as_view())
]
