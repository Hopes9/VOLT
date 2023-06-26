from django.contrib.auth.models import AnonymousUser
from django.test import Client, TestCase
from django.urls import reverse
from django.test import RequestFactory, TestCase

from accounts.models import User
from product.views import OpenProduct


class ProductMainTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_product_main_view(self):
        response = self.client.get("/product/")
        self.assertEqual(response.status_code, 200)


class SearchProductTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.find = "Катушка"

    def test_search_product_view(self):
        response = self.client.post("/product/search/", data={"find": self.find})
        self.assertEqual(response.status_code, 200)


class OpenProductTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user, _ = User.objects.get_or_create(
            phone='89666666', password='top_secret8!A')
        self.product_id = 1

    def test_open_product_view(self):
        request = self.factory.get(f"/product/1/")

        request.user = self.user
        response = OpenProduct.as_view()(request, self.product_id)
        self.assertEqual(response.status_code, 200)


class FavesProductTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_faves_product_view(self):
        response = self.client.post("/product/favs/", data={"ids": "12,123,321"})
        self.assertEqual(response.status_code, 200)


class CatalogTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_catalog_view(self):
        response = self.client.get("/product/catalog/")

        self.assertEqual(response.status_code, 200)


class CatalogValuesTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.limit = 10
        self.page = 1

    def test_catalog_values_view(self):
        response = self.client.post(f"/product/catalog/values/{self.limit}/{self.page}/")
        self.assertEqual(response.status_code, 200)


class GetFiltersTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_filters_view(self):
        response = self.client.post("/product/catalog/getFilters/")
        self.assertEqual(response.status_code, 200)


class GetFiltersIntTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.feature = 1

    def test_get_filters_int_view(self):
        response = self.client.post(f"/product/catalog/getFilters/{self.feature}")
        self.assertEqual(response.status_code, 200)
