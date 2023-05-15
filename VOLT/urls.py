from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from . import settings
from .views import LogoutView, LogoutAllView, CookieTokenObtainPairView, CookieTokenRefreshView, All_product, \
    Rassilka_off

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# from rosetta
urlpatterns = [
      path("admin/", admin.site.urls),

      path("swagger", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
      path("redoc", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),


      path("jwt", CookieTokenObtainPairView.as_view(), name="token_obtain_pair"),
      path("jwt/refresh", CookieTokenRefreshView.as_view(), name="token_refresh"),

      path("logout/", LogoutView.as_view(), name="auth_logout"),
      path("logout_all/", LogoutAllView.as_view(), name="auth_logout_all"),

      path("profile/", include("accounts.urls")),

      path("order/", include("order.urls")),
      path("basket/", include("basket.urls")),
      path("product/", include("product.urls")),

      path("all_product/", All_product.as_view()),
      re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATICFILES_DIRS}, name='static'),
      re_path(r'^staticfiles/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='staticfiles'),
      path('sberbank/', include('sberbank.urls')),
      path("rassilka_off/", Rassilka_off.as_view()),
]
