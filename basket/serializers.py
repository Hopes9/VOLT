from rest_framework import serializers

from basket.models import Basket


class Basket_serializers(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = "__all__"
