from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.db import connection

from VOLT import settings
from accounts.models import User
from order.chek import chek
from order.email_form import oplata
from order.lang import order_dict
from product.func import dict_fetch_all


def rows_email(order):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
           SELECT orderList.id,
           orderList.order_id,
           orderList.product_id,
           orderList.money,
           orderList.count
           FROM order_order_list orderList
           inner join product_product pp on orderList.product_id = pp.id
             WHERE orderList.order_id = {order.id}
            """)
        ros = dict_fetch_all(cursor)

    with connection.cursor() as cursor:
        cursor.execute(f"""SELECT "order_order"."id",
           order_order."id_user_id",
           order_order."status",
           order_order."data_order",
           order_order."address",
           order_order."chek",
           order_order."delivery_id",
           order_order."pay",
           order_order."pay_online",
           order_order."sum",
           order_order."date_close",
           order_order."discount",
           order_order."count_product", 
            sp.details
            FROM "order_order"
            left JOIN sberbank_payment sp on order_order.id = sp.order_id
            WHERE "order_order"."id" = {order.id}""")
        rog = dict_fetch_all(cursor[0])
    return ros, rog


def send_my_email_create(order):
    values, orders = rows_email(order)
    user_u = User.objects.get(id=orders["id_user_id"])

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_u.email]
    html_message = oplata(values, order, user_u)

    email = EmailMessage(
        order_dict["new_order"],
        html_message,
        from_email,
        recipient_list
    )
    email.content_subtype = "html"
    email.send()


    send_my_email_create_she(order, html_message)


def send_my_email_create_she(order, oplat):
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [settings.EMAIL_HOST_USER]
    html_message = oplat

    html_message += f"Ссылка на изменение статуса заказа\nhttps://api.tm-she.com/admin/order/order/{order.id}/change/\n"

    email = EmailMessage(
        f"Оформили заказ {order.order_id}",
        html_message,
        from_email,
        recipient_list
    )
    email.content_subtype = "html"
    email.send()


def send_my_email_pay(lang, order):

    values, orders = rows_email(order)
    user_u = User.objects.get(id=orders["id_user_id"])

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_u.email]
    html_message = oplata(values, order, user_u, to_pay=True)

    email = EmailMessage(
        order_dict[lang]["new_order"],
        html_message,
        from_email,
        recipient_list
    )
    email.content_subtype = "html"
    email.send()


def send_for_user_link_pay_true(order):
    values, orders = rows_email(order)
    user_u = User.objects.get(id=orders["id_user_id"])

    body = "Пользователь оплатил заказ "
    body += f"{order_dict['number']}: {order.order_id}\n"
    body += f"{order_dict['order_user']}: {user_u.get_full_name()}\n"
    body += f"{order_dict['sposoborder']}: {order.delivery}\n"
    body += f"{order_dict['phone']}: {user_u.phone}\n"
    body += f"{order_dict['sum']}: {order.sum}\n"
    send_mail(f'{order_dict["order"]} {order.order_id}', body, settings.EMAIL_HOST_USER,
              [settings.EMAIL_HOST_USER])

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_u.email]
    html_message = chek(values, order, user_u)

    email = EmailMessage(
        order_dict["new_order"],
        html_message,
        from_email,
        recipient_list
    )
    email.content_subtype = "html"
    email.send()

