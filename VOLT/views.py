from django.http import FileResponse
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from VOLT.settings import COOKIE_MAX_AGE
from accounts.models import Faq, NewCall, NewPartner, Politics, User
from accounts.serializers import FaqSerializer, NewCallSerializer, NewPartnerSerializer, PoliticsSerializer
from product.models import Product

from accounts.serializers import JSONWebTokenSerializer

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)


class docxView(APIView):
    @staticmethod
    def get(request):
        return FileResponse(
            open("staticfiles/docx/Политика_конфиденциальности_+_Согласие_на_обработку_ПД_PollHub.docx", "rb"))


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = self.context["request"].COOKIES.get("refresh_token")
        if attrs["refresh"]:
            return super().validate(attrs)
        else:
            raise InvalidToken("No valid token found in cookie \"refresh_token\"")


class CookieTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            response.set_cookie("refresh_token", response.data["refresh"], max_age=COOKIE_MAX_AGE, httponly=False)
            del response.data["refresh"]
        return super().finalize_response(request, response, *args, **kwargs)


class LoginJWT(JSONWebTokenSerializer):
    def validate(self, attrs):
        credentials = {
            'email': '',
            'phone': '',
            'password': attrs.get("password")
        }
        user_obj = User.objects.filter(email=attrs.get("email")).first() or User.objects.filter(phone=attrs.get("phone")).first()
        print(user_obj, "ASd")
        if user_obj:
            credentials['phone'] = user_obj.phone

        return super().validate(credentials)


class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get("refresh"):
            response.set_cookie("refresh_token", response.data["refresh"], max_age=COOKIE_MAX_AGE, httponly=False)
            del response.data["refresh"]
        return super().finalize_response(request, response, *args, **kwargs)

    serializer_class = CookieTokenRefreshSerializer


class All_product(APIView):
    @staticmethod
    def get(request):
        return Response(Product.objects.all().order_by("id").values("id"))


class Rassilka_off(APIView):
    @staticmethod
    def get(request):
        use = User.objects.get(id=request.GET.get("id"))
        use.rassilka = False
        use.save()
        return Response("Рассылка отменена")


class FaqApiview(ListAPIView):
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer


class NewCallApiview(ListAPIView):
    queryset = NewCall.objects.all()
    serializer_class = NewCallSerializer


class NewPartnerApiview(ListAPIView):
    queryset = NewPartner.objects.all()
    serializer_class = NewPartnerSerializer


class PoliticsApiview(ListAPIView):
    queryset = Politics.objects.all()
    serializer_class = PoliticsSerializer
