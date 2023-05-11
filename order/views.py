import json
import uuid

import requests
from django.db import connection
from django.db.models import Q
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from VOLT import settings
from VOLT.settings import Token_cdek
from basket.models import Basket
from product.models import Product
from sberbank.models import Payment
from sberbank.service import BankService
from order.func import send_my_email_create
from order.models import Order, Order_list, Status
from product.func import dict_fetch_all, get_secret_key_


@permission_classes([IsAuthenticated])
class Post_order(APIView):
    def post(self, request):

        basket_list = Basket.objects.filter(id_user_id=request.user.id)
        basket = basket_list.values_list("product_id")
        if len(basket) == 0:
            return Response({"detail": "Нет товаров"})
        Product_list = Product.objects.filter(id__in=basket)

        price_sber = 0.0
        count_product = 0
        #
        # if request.data.get("pay_online") and request.data.get("address") and request.data.get("delivery"):
        #     pay_online = json.loads(request.data.get("pay_online").lower())
        #     for i in Product_list:
        #         count_product += i["count"]
        #
        #         if int(i["discount"]) != 0:
        #             if request.user.distribution is True:
        #                 price_sber += (float(i["price"]) - (float(i["price"]) * float(i["distribution_count"] / 100))) * int(i["count"])
        #                 continue
        #             price_sber += float(i["price"]) - (float(i["price"]) * (i["discount"] / 100))
        #         else:
        #             if request.user.distribution is True:
        #                 price_sber += (float(i["price"]) - (float(i["price"]) * float(i["distribution_count"] / 100))) * int(i["count"])
        #                 continue
        #             price_sber += float(i["price"]) * int(i["count"])
        #
        #     order = Order.objects.create(id_user=request.user,
        #                                  order_id=f"{request.user.id}",
        #                                  status=Status.CREATED,
        #                                  address=request.data.get("address"),
        #                                  chek=None,
        #                                  pay=False,
        #                                  pay_online=pay_online,
        #                                  sum_sber=price_sber,
        #                                  discount=request.user.distribution,
        #                                  delivery_id=request.data.get("delivery"),
        #                                  count_product=count_product
        #                                  )
        #
        #     order.order_id = f"{get_secret_key_()}-{order.id}"
        #     order.save()
        #     for i in row:
        #         money = i["price"]
        #         money = float(money) - float(money) * float(i["distribution_count"] / 100)
        #         Order_list.objects.create(product_id=i["product_id"],
        #                                   order=order,
        #                                   money=money,
        #                                   count=i["count"])
        #     order_values = dict(Order.objects.filter(id=order.id).values().first())
        #     ros = Order_list.objects.filter(order_id=order.id).values()
        #     order_values.update(order_list=ros)
        #
        #     send_my_email_create(order)
        #
        #     return Response(order_values)
        return Response(Product_list.values())


def chek_uuid(uuid_):
    try:
        if uuid.UUID(uuid_):
            return True
    except ValueError:
        return False


@permission_classes([IsAuthenticated])
class My_orders(APIView):
    def get(self, request, lang):
        if request.GET.get("bank_id") is not None or request.GET.get("id") is not None:
            if request.GET.get('id') is None:
                order_id = ""
            else:
                order_id = f"and order_.id = {int(request.GET.get('id'))}"
            if request.GET.get('bank_id') is None:
                bank_id = ""
            else:
                if not chek_uuid(request.GET.get('bank_id')):
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    bank_id = f"and sp.bank_id = '{request.GET.get('bank_id')}'"

            try:
                rows = f"""select order_.id, order_.order_id, order_.status, data_order, address, chek, amount, sum, date_close, pay, order_.pay_online, order_.discount, order_.delivery_id, order_.count_product, order_.lang as price_currency, sp.details
                        from order_order order_ 
                        left join sberbank_payment sp on order_.id = sp.order_id 
                        where order_.id_user_id = {request.user.id} {bank_id} {order_id} """

                with connection.cursor() as cursor_1:
                    cursor_1.execute(rows)
                    row = dictfetchall(cursor_1)
                print(type(row), row)
                if len(row) is None:
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    row = row[0]
                    if row["pay_online"] is not None:
                        if row["status"] == 1:
                            if row["details"] is not None:
                                f = json.loads(row["details"])
                                row.update(details=f["redirect_url"])
                        else:
                            row.pop("details")
                    if row['price_currency'] == 0:
                        row['price_currency'] = "RUB"
                    else:
                        row['price_currency'] = "USD"

                with connection.cursor() as cursor_2:
                    cursor_2.execute(f"""SELECT 
                    order_order_list."id",
                    product_product."id" as product_id,
                    product_product_ml."ml",
                    pp_tra.name,
                    ppct.color,
                    order_order_list."money",
                    order_order_list."count",
                    product_product."article",
                    ppim."image"                    
                    FROM "order_order_list"
                         INNER JOIN "product_product_more" ON order_order_list.product_id = product_product_more.id
                        LEFT OUTER JOIN "product_product_ml" ON ("product_product_more"."ml_id" = "product_product_ml"."id")
                         INNER JOIN "product_product" ON ("product_product_more"."product_id_id" = "product_product"."id")
                         inner join product_product_image_main ppim on product_product.id = ppim.image_product_id
                         INNER JOIN product_product_color ppc on ppc.id = product_product.color_id
                         INNER JOIN product_product_color_translation ppct on ppc.id = ppct.master_id
                         INNER JOIN product_product_translation pp_tra on product_product.id = pp_tra.master_id 
                         WHERE "order_order_list"."order_id" = {row["id"]} and pp_tra.language_code = '{lang}' and ppct.language_code = '{lang}' and ppim.show = True""")
                    ror = dictfetchall(cursor_2)
                print(ror)
                row.update(order_list=ror)
                return Response(row)
            except Exception as e:
                return Response({"error": e})
        else:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"select order_.id, order_.order_id, order_.status, data_order, sp.bank_id, address, chek, amount, sum,date_close, pay, order_.pay_online, order_.discount, order_.delivery_id, order_.count_product, order_.lang as price_currency "
                    f"from order_order order_ "
                    f"left join sberbank_payment sp on order_.id = sp.order_id "
                    f"where id_user_id = {request.user.id} order by order_.id desc ")
                row = dictfetchall(cursor)
                for i in row:
                    cursor.execute(
                        f"""SELECT product_product_image_main.image
                        FROM order_order_list
                        INNER JOIN product_product_more
                        ON order_order_list.product_id = product_product_more.id
                        INNER JOIN product_product
                        ON product_product_more.product_id_id = product_product.id
                        LEFT OUTER JOIN product_product_image_main
                        ON product_product.id = product_product_image_main.image_product_id
                        WHERE "order_order_list"."order_id" = {i["id"]} and product_product_image_main.show = TRUE""")
                    ror = dictfetchall(cursor)
                    i.update(order_list=ror)
                    if i["price_currency"] == 0:
                        i.update(price_currency="RUB")
                    else:
                        i.update(price_currency="USD")
            return Response(row)


class Create_pay(APIView):
    def get(self, request):
        if request.GET.get('order') is None:
            return Response(status=status.HTTP_204_NO_CONTENT)
        order_id = request.GET.get('order')
        order_ = get_object_or_404(Order, id=order_id)
        paym = Payment.objects.filter(order=order_id).last()
        if paym is None:
            svc = BankService(settings.MERCHANT_KEY)
            payment, url = svc.pay(order_.sum_sber, params={'foo': 'bar',
                                                            "admin_text": f"https://api.tm-she.com/admin/order/order/{order_.id}/change/"},
                                   client_id=order_.id_user.id,
                                   description=f"Оплата заказа {order_.order_id}",
                                   order_id=order_.id)
            return HttpResponseRedirect(url)
        else:
            from sberbank.models import Status
            svc = BankService(settings.MERCHANT_KEY)
            payment = svc.check_status(paym.uid)
            if payment.status != Status.FAILED:
                return HttpResponseRedirect(payment.details["redirect_url"])
            else:
                Payment.objects.filter(order=order_id).delete()
                svc = BankService(settings.MERCHANT_KEY)
                payment, url = svc.pay(order_.sum_sber, params={'foo': 'bar',
                                                                "admin_text": f"https://api.tm-she.com/admin/order/order/{order_.id}/change/"},
                                       client_id=order_.id_user.id,
                                       description=f"Оплата заказа {order_.order_id}",
                                       order_id=order_.id)
                return HttpResponseRedirect(url)


class Cdek_order(APIView):
    def post(self, request):
        try:
            if request.data.get("city") is None:
                return Response("Нет города city")
            url_ = "https://api.cdek.ru/v2/calculator/tariff"

            payload_ = json.dumps({
                "tariff_code": 136,
                "currency": 1,
                "to_location": {
                    "address": request.data.get("city")
                },
                "from_location": {
                    "address": "Белгород"
                },
                "packages": [
                    {
                        "height": 20,
                        "length": 20,
                        "weight": 500,
                        "width": 10,
                    }
                ],
                "type": 1
            })
            headers_ = {
                'Authorization': f'Bearer {Token_cdek.t}',
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url_, headers=headers_, data=payload_)
            text = json.loads(response.text)
            try:
                if text["requests"][0]["errors"][0]["code"] == "v2_token_expired" or text["requests"][0]["errors"][0]["code"] == "v2_authorization_incorrect":
                    url = "https://api.cdek.ru/v2/oauth/token"
                    payload = {'client_id': 'wgRPShgRZq5vV3MoEoibUHHXTE4cWtNm',
                               'client_secret': 'i6CsZE9b2xQpoMfZPW1hm3VleYcNIEuE',
                               'grant_type': 'client_credentials'}
                    headers = {}
                    files = []
                    response = requests.request("POST", url, headers=headers, data=payload, files=files)
                    text = json.loads(response.text)
                    Token_cdek.t = text["access_token"]
                    headers_ = {
                        'Authorization': f'Bearer {Token_cdek.t}',
                        'Content-Type': 'application/json'
                    }
                    response = requests.request("POST", url_, headers=headers_, data=payload_)
                    text = json.loads(response.text)

                    return Response({"total_sum": text["total_sum"] + 100})
            except:
                return Response({"total_sum": text["total_sum"] + 100})
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
