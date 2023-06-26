from rest_framework import serializers

from accounts.models import Faq, NewCall, NewPartner, Politics, User


class userProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "phone", "first_name", "last_name", "middle_name", "user_image", "distribution"]


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


class CreateUserSerializer(serializers.Serializer):
    phone = serializers.IntegerField(required=True)
    code = serializers.IntegerField(required=True)
    password = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    middle_name = serializers.CharField(required=True)


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = "__all__"


class NewCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewCall
        fields = "__all__"


class NewPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewPartner
        fields = "__all__"


class PoliticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Politics
        fields = "__all__"
