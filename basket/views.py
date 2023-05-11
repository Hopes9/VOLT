from django.db import connection
from django.db.models import Sum
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from product.func import dict_fetch_all
from product.models import Product
from .models import Basket
from .serializers import Basket_serializers


@permission_classes([IsAuthenticated])
class Basket_APIView(APIView):
    instance = Basket.objects.all()
    serializer_class = Basket_serializers

    def get(self, request):
        basket_list = Basket.objects.filter(id_user_id=request.user.id)
        basket = basket_list.values_list("product_id")
        if len(basket) == 0:
            return Response({"detail": "Нет товаров"})
        Product_list = Product.objects.filter(id__in=basket)

        return Response(Product_list.values())

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


class Basket_APIView_new(APIView):
    instance = Basket.objects.all()
    serializer_class = Basket_serializers

    def post(self, request):
        ids = request.GET.get("ids")
        id_list = str(ids).split(",")

        products = Product.objects.filter(id__in=id_list)

        for product in products:
            basket_product = Basket(id_user=request.user.id, product_id=product)
            basket_product.save()

        basket_items = (
            Basket.objects
            .filter(id_user=request.user.id)
            .values()
            .annotate(count=Sum('count'))
        )

        data = list(basket_items)
        total_price = sum(item['count'] * item['product__price'] for item in data)
        data.append({'total_price': total_price})

        return Response(data)

@permission_classes([IsAuthenticated])
class Basket_work(RetrieveUpdateDestroyAPIView):
    queryset = Basket.objects.all()
    serializer_class = Basket_serializers
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = Basket_serializers(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()


        basket_items = (
            Basket.objects
            .filter(id_user=request.user.id)
            .values()
            .annotate(count=Sum('count'))
        )

        data = list(basket_items)
        total_price = sum(item['count'] * item['product__price'] for item in data)
        data.append({'total_price': total_price})

        return Response(data)

@permission_classes([IsAuthenticated])
class Basket_get_price_APIView(APIView):
    queryset = Basket.objects.all()
    serializer_class = Basket_serializers

    def get(self, request, lang):
        with connection.cursor() as cursor:
            cursor.execute(
                f"""select bas.id, count, buy_now, product_id,
                from basket_basket bas
                where id_user_id = {request.user.id} and bas.buy_now = True""")

            row = dict_fetch_all(cursor)
        price = 0.0
        for i in row:
            if int(i["discount"]) != 0:
                if request.user.distribution is True:
                    price += (float(i["price"]) - (float(i["price"]) * float(i["distribution_count"] / 100))) * int(
                        i["count"])
                    continue
                price += float(i["price"]) - (float(i["price"]) * (i["discount"] / 100))
            else:
                if request.user.distribution is True:
                    price += (float(i["price"]) - (float(i["price"]) * float(i["distribution_count"] / 100))) * int(
                        i["count"])
                    continue
                price += float(i["price"]) * int(i["count"])
        return Response(price)
