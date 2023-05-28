from django.urls import path

from product.views import Open_product, Update_prodat, Update_pricat, UpdateCatalog, catalog, getFilters, getFiltersInt

from .views import Search_product, Open_product, FavesProduct, \
    catalog_values, Product_

urlpatterns = [
    path("", Product_.as_view()),
    path("search/", Search_product.as_view()),
    path("<int:pk>/", Open_product.as_view()),
    path("favs/", FavesProduct.as_view()),
    path("catalog/", catalog.as_view()),
    path("catalog/values/<int:limit>/<int:page>/", catalog_values.as_view()),
    path("catalog/getFilters/", getFilters.as_view()),
    path("catalog/getFilters/<int:feature>", getFiltersInt.as_view()),

    path("updateCatalog/", UpdateCatalog.as_view()),
    path("update/prodat/", Update_prodat.as_view()),
    path("update/pricat/", Update_pricat.as_view()),
]
