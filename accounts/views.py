import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from VOLT.settings import COOKIE_MAX_AGE
from accounts.models import User, Confirm_phone, Agreement
from accounts.permissions import IsOwnerProfileOrReadOnly
from accounts.phone import call_phone
from accounts.serializers import userProfileSerializer, ChangePasswordSerializer

scheduler = BackgroundScheduler()
scheduler.start()


class userProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = userProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerProfileOrReadOnly]

    def get(self, request):
        instance = request.user
        serializer = userProfileSerializer(instance)
        data = serializer.data
        return Response(data)

    def patch(self, request):
        serializer = userProfileSerializer(instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        try:
            u = User.objects.get(id=request.user.id)
            u.delete()
            return Response("The user is deleted")
        except User.DoesNotExist:
            return Response("User does not exist")
        except Exception as e:
            return Response({'err': str(e)})


class Confirm_phone_api_view(APIView):
    def post(self, request):
        phone = request.data.get("phone")
        if phone is not None:
            return generate_phone_code(phone=phone)
        else:
            return Response({"detail": "Нужно передать номер телефона"}, status=status.HTTP_404_NOT_FOUND)


class Confirm_code_api_view(APIView):
    def post(self, request):
        row = request.data
        phone = row.get("phone")
        code = row.get("code")
        first_name = row.get("first_name")
        last_name = row.get("last_name")
        if (phone and code) is not None:
            if int(code) in Confirm_phone.objects.filter(phone=phone).values_list("code", flat=True):
                user = User.objects.filter(phone=phone).first()
                if user is None:
                    if (first_name and last_name) is None:
                        user = User.objects.create(phone=phone)
                    else:
                        user = User.objects.create(phone=phone, first_name=first_name, last_name=last_name)

                    # user.set_password(password)
                    user.save()
                # Confirm_phone.objects.filter(phone=phone).delete()
                refresh = RefreshToken.for_user(user)
                response = Response({"refresh_token": str(refresh), "access_token": str(refresh.access_token)},
                                    status=status.HTTP_200_OK)
                if response.data.get("refresh"):
                    del response.data["refresh"]
                response.set_cookie("refresh_token", refresh, max_age=COOKIE_MAX_AGE,
                                    httponly=True)
                return response
            else:
                return Response({"detail": "Код не верный"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Нужно передать phone, code"}, status=status.HTTP_404_NOT_FOUND)


def delete_from_confirm(phone, code):
    Confirm_phone.objects.filter(phone=phone, code=code).delete()


def generate_phone_code(phone):
    code = call_phone(phone)
    Confirm_phone.objects.create(code=code, phone=phone, ucaller_id=code)

    scheduler.add_job(delete_from_confirm, 'date', [phone, code],
                      run_date=datetime.datetime.now() + datetime.timedelta(minutes=2))
    return Response({"info": "Код отправлен, код работает 2 мин", "text": code}, status=status.HTTP_200_OK)


class Reset_password(APIView):
    def post(self, request):
        phone = request.data.get("phone")
        if phone is not None:
            return generate_phone_code(phone)
        else:
            return Response({"detail": "Нужно передать телефон"}, status=status.HTTP_400_BAD_REQUEST)


class Reset_password_confirm(APIView):
    def post(self, request):
        row = request.data
        phone = row.get("phone")
        password = row.get("password")
        code = row.get("code")
        if (phone and password and code) is not None:
            confirm_phone = Confirm_phone.objects.filter(phone=phone)

            if int(code) in list(Confirm_phone.objects.filter(phone=phone).values_list("code", flat=True)):
                confirm_phone.delete()
                user = User.objects.get(phone=phone)
                serializer = ChangePasswordSerializer(user, data={"password": password, "phone": phone})
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({"info": "Пароль изменён"}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Код не верный"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "Нужно передать phone, code, password"}, status=status.HTTP_404_NOT_FOUND)
