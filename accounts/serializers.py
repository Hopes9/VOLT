
from rest_framework import serializers

from accounts.models import User


class userProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "phone", "first_name", "last_name", "user_image", "distribution"]


class userProfileSerializer_a(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = "__all__"


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    phone = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("phone", "password",)

    def update(self, instance, validated_data):
        instance.set_password(raw_password=validated_data["password"])
        instance.save()
        return instance


