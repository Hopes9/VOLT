from django.urls import path
from .views import userProfileDetailView, Confirm_phone_api_view, Confirm_code_api_view, \
    Reset_password, ResetPasswordConfirm, CreateUser

urlpatterns = [
    path("", userProfileDetailView.as_view(), name="profile"),
    # path("<str:lang>/agreement/", Agreement_view.as_view()),
    path("confirm_phone", Confirm_phone_api_view.as_view()),
    path("confirm_code", Confirm_code_api_view.as_view()),
    path("reset_password", Reset_password.as_view()),
    path("reset_password_confirm", Confirm_code_api_view.as_view()),
    path("reset_password_finish", ResetPasswordConfirm.as_view()),
    
    path("createUser", CreateUser.as_view())
]
