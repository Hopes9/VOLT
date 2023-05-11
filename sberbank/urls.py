from django.urls import re_path
from sberbank import views

urlpatterns = [
    re_path('payment/callback', views.callback),
    re_path('payment/success', views.redirect, {'kind': 'success'}),
    re_path('payment/fail', views.redirect, {'kind': 'fail'}),
    re_path('payment/status/(?P<uid>[^/]+)/', views.StatusView.as_view()),
    re_path('payment/bindings/(?P<client_id>[^/]+)/', views.BindingsView.as_view()),
    re_path('payment/binding/(?P<binding_id>[^/]+)/', views.BindingView.as_view()),
    re_path('payment/history/(?P<client_id>[^/]+)/', views.GetHistoryView.as_view()),
]
