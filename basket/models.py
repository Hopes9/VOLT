from __future__ import unicode_literals

from django.db import models

from accounts.models import User
from product.models import Product


class Basket(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    buy_now = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return f'{self.product} | x{self.count}'


class Like(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
