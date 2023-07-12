
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.tokens import RefreshToken

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


class Serializer(serializers.Serializer):
    @property
    def object(self):
        return self.validated_data

class JSONWebTokenSerializer(Serializer):
    """
    Serializer class used to validate a username and password.

    'username' is identified by the custom UserModel.USERNAME_FIELD.

    Returns a JSON Web Token that can be used to authenticate later calls.
    """

    def __init__(self, *args, **kwargs):
        """
        Dynamically add the USERNAME_FIELD to self.fields.
        """
        super(JSONWebTokenSerializer, self).__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField(write_only=True)

    @property
    def username_field(self):
        return get_user_model().USERNAME_FIELD

    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)

                refresh = RefreshToken.for_user(user)
                
                return {
                    "refresh_token": str(refresh), "access_token": str(refresh.access_token)
                }
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)
