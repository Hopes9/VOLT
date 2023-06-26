from __future__ import unicode_literals
from django.utils.translation import gettext as _
from django.db import models
from enum import IntEnum
from product.models import Product

from .func import *


class Choice(IntEnum):
    @classmethod
    def choices(cls):
        return [(x.value, x.name) for x in cls]


class Status(Choice):
    CREATED = 0
    ON_PAY = 1
    Pleasantly = 2
    Delivery = 3
    SUCCEEDED = 4
    FAILED = 5
    REFUNDED = 6
    Completed = 7

    def __str__(self):
        return str(self.value)


class Delivery(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_text = models.TextField()

    def __str__(self):
        return str(self.delivery_text)

    def __unicode__(self):
        return self.id


class Order(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_name = models.TextField()
    status = models.PositiveSmallIntegerField(_("status"), choices=Status.choices(),
                                              default=Status.CREATED, db_index=True)
    data_order = models.DateTimeField(_("Дата создания"), auto_now_add=True)
    address = models.TextField(_("Адрес"), )
    chek = models.TextField(_("Чек"), null=True, blank=True)

    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    pay = models.BooleanField(_("Оплачено"), default=False)
    pay_online = models.BooleanField(_("Оплата онлайн"), default=None, null=True, blank=True)
    # pay_online_secret_code = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
    sum = models.FloatField(_("Сумма"), )
    date_close = models.DateTimeField(_("Дата закрытия"), null=True, default=None, blank=True)
    discount = models.IntegerField(_("Скидка"), default=0, null=True, blank=True)
    count_product = models.IntegerField(_("Кол-во продуктов"), default=0, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.date_close:
            self.date_close = None

        super(Order, self).save(*args, **kwargs)

        if self.status == 4:
            if self.pay_online:
                send_for_user_link_pay_true(self)

    def __unicode__(self):
        return self.id

    def __str__(self):
        return self.order_id


class Order_list(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    money = models.FloatField()
    count = models.IntegerField(default=1)

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.product)
