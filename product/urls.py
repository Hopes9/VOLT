from django.urls import path

from product.views import UpdateCatalog, Catalog, GetFilters, GetFiltersInt
from .views import SearchProduct, OpenProduct, FavesProduct, \
    CatalogValues, ProductMain

urlpatterns = [
    path("", ProductMain.as_view()),
    path("search/", SearchProduct.as_view()),
    path("<int:pk>/", OpenProduct.as_view()),
    path("favs/", FavesProduct.as_view()),
    path("catalog/", Catalog.as_view()),
    path("catalog/values/<int:limit>/<int:page>/", CatalogValues.as_view()),
    path("catalog/getFilters/", GetFilters.as_view()),
    path("catalog/getFilters/<int:feature>", GetFiltersInt.as_view()),

    path("updateCatalog/", UpdateCatalog.as_view()),
]
