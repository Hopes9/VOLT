from pprint import pprint

from django.db import connection
from django.db.models import Sum
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from product.func import dict_fetch_all
from product.models import Product
from .func import sumPrice
from .models import Basket
from .serializers import Basket_serializers


@permission_classes([IsAuthenticated])
class Basket_APIView(APIView):
    def get(self, request):
        basket_items = Basket.objects.filter(id_user=request.user.id).values("id",
                    "id_user",
                    "product_id",
                    "product__ProductName",
                    "product__discount",
                    "product__image",
                    "product__discount",
                    "product__RetailPrice",
                    "count",
                    "buy_now")

        if len(basket_items) == 0:
            return Response({"detail": "Нет товаров"})

        response = sumPrice(basket_items)

        return Response(response)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data["id_user"] = request.user.id
        serializer = Basket_serializers(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        Basket.objects.filter(id_user=request.user.id).delete()
        return Response(status=status.HTTP_404_NOT_FOUND)

@permission_classes([IsAuthenticated])
class Basket_APIView_new(APIView):

    def post(self, request):
        ids = request.data.get("ids")
        id_list = str(ids).split(",")
        if ids:
            products = Product.objects.filter(id__in=id_list)

            for product in products:
                basket_product = Basket(id_user_id=request.user.id, product_id=product.id)
                basket_product.save()

            basket_items = (
                Basket.objects
                .filter(id_user=request.user.id)
                .values("id",
                        "id_user",
                        "product_id",
                        "product__ProductName",
                        "product__image",
                        "product__discount",
                        "product__RetailPrice",
                        "count",
                        "buy_now")
            )
            response = sumPrice(basket_items)

            return Response(response)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
class Basket_work(RetrieveUpdateDestroyAPIView):
    queryset = Basket.objects.all()
    serializer_class = Basket_serializers
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = Basket_serializers(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        basket_items = Basket.objects.filter(id_user=request.user.id).values("id",
                    "id_user",
                    "product_id",
                    "product__ProductName",
                    "product__discount",
                    "product__image",
                    "product__discount",
                    "product__RetailPrice",
                    "count",
                    "buy_now")
        response = sumPrice(basket_items)
        return Response(response)

@permission_classes([IsAuthenticated])
class Basket_get_price_APIView(APIView):
    queryset = Basket.objects.all()
    serializer_class = Basket_serializers

    def get(self, request):
        basket_items = Basket.objects.filter(id_user=request.user.id).values("id",
                    "id_user",
                    "product_id",
                    "product__ProductName",
                    "product__discount",
                    "product__image",
                    "product__discount",
                    "product__RetailPrice",
                    "count",
                    "buy_now")
        response = sumPrice(basket_items)
        return Response(response)
