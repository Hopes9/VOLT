from django.urls import path

from .views import Basket_APIView, Basket_work, Basket_get_price_APIView, Basket_APIView_new

urlpatterns = [
    path("", Basket_APIView.as_view()),
    path("new/", Basket_APIView_new.as_view()),
    path("<int:pk>/", Basket_work.as_view()),
    path("price/", Basket_get_price_APIView.as_view()),
]
