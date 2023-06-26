import json
import math
from datetime import datetime

from django.db.models import Count, Max, Min, OuterRef, Q, Subquery, Sum
from django.db.models.functions import Length
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from VOLT.settings import BASE_DIR
from order.models import Order_list
from product.ftp import getfile
from product.func import chek_list_int, update_catalog
from product.models import Brand, CatalogBrochure, CertificateInfo, Country, FeatureETIMDetails, \
    FeatureETIMDetails_Data, Product, Product_image, Product_video, RelatedProd, RsCatalog, Series
from product.serializers import CatalogBrochureSerializer, CertificateInfoSerializer, CountrySerializer, \
    ProductSerializer, Product_imageSerializer, Product_videoSerializer, RelatedProdSerializer, RsCatalogSerializer


class ProductMain(APIView):
    @staticmethod
    def get(request):
        offset = 0
        limit = 30
        if request.data.get("offset") is not None:
            offset = int(request.data.get("offset"))

        if request.data.get("limit") is not None:
            limit = int(request.data.get("limit"))

        products = Product.objects.order_by('id')[offset:limit]  # offset 9, limit 30
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class SearchProduct(APIView):
    @staticmethod
    def post(request):
        if request.data.get("find") is not None:
            st = request.data.get("find")
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
        if request.data.get("limit") is not None:
            limit = request.GET.get("limit")
            products = Product.objects.filter(Q(ProductName__icontains=st) | Q(VendorProdNum__icontains=st))[:limit]
        else:
            products = Product.objects.filter(Q(ProductName__icontains=st) | Q(VendorProdNum__icontains=st))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class FavesProduct(APIView):
    @staticmethod
    def post(request):
        if not request.data.get("ids"):
            return Response(status=status.HTTP_404_NOT_FOUND)

        id_list = request.data.get("ids").split(",")
        products = Product.objects.filter(id__in=id_list).values()

        return Response(products)


class Catalog(APIView):
    @staticmethod
    def get(request):
        with open("catalog.json", "r", encoding="UTF-8") as f:
            data = f.read()
        data = json.loads(data)
        return Response(data, status=status.HTTP_200_OK)


class GetFilters(APIView):
    @staticmethod
    def post(request):
        level2 = request.data.get("Level2")
        level3 = request.data.get("Level3")
        level4 = request.data.get("Level4")
        price_min = request.data.get("price_min")
        price_max = request.data.get("price_max")
        brand = request.data.get("brand")
        series = request.data.get("series")
        feature = request.data.get("feature")

        rs_catalog = RsCatalog.objects.all()
        if level2:
            rs_catalog = rs_catalog.filter(Level2ID=level2)
        if level3:
            rs_catalog = rs_catalog.filter(Level3ID=level3)
        if level4:
            rs_catalog = rs_catalog.filter(Level4ID=level4)
        if not (level4 or level3 or level2):
            return Response({"Error": "GET Level"})

        row_ = Product.objects.filter(id__in=rs_catalog.values_list("product_catalog", flat=True))
        if price_min:
            row_ = row_.filter(RetailPrice__gte=price_min)
        if price_max:
            row_ = row_.filter(RetailPrice__lte=price_max)

        if brand:
            k = chek_list_int(brand)
            if len(k) != 0:
                row_ = row_.filter(brand__in=k)
            else:
                return Response(status.HTTP_204_NO_CONTENT)
        if series:
            k = chek_list_int(series)
            if len(k) != 0:
                row_ = row_.filter(Series__in=k)
            else:
                return Response(status.HTTP_204_NO_CONTENT)

        filters = {"others": []}
        if feature:
            try:
                feature = json.loads(feature)
                list_feature_id = [h["feature_id"] for h in feature]
                data = FeatureETIMDetails.objects.filter(id__in=list_feature_id)

                datas = FeatureETIMDetails_Data.objects.filter(featureETIMDetails__in=data.values("id"))
                for h in feature:
                    datas = datas.filter(featureValue__in=h["service"])
                row_ = row_.filter(id__in=datas.values("featureETIMDetails_product_id"))
            except Exception as e:
                return Response({"ERROR": "Feature Example: {'1567': ['300']}", "service": str(e)},
                                status=status.HTTP_400_BAD_REQUEST)
        filter_m = FeatureETIMDetails.objects.filter(featureetimdetails_data__featureETIMDetails_product__id__in=
                                                     row_.values_list("id", flat=True)) \
            .annotate(count=Count("featureName")).order_by("-count")
        if filter_m.count() > 20:
            filter_m = filter_m[:20]
        filters["filters"] = filter_m.values()

        filters["others"] = [{"name": "Brands",
                              "values": Brand.objects.filter(id__in=row_.values_list("brand", flat=True)).values(
                                  "id", "name")},
                             {"name": "Series",
                              "values": Series.objects.filter(id__in=row_.values_list("Series", flat=True)).values(
                                  "id", "name")}]
        return Response(filters)


class GetFiltersInt(APIView):
    @staticmethod
    def post(request, feature):
        level2 = request.data.get("Level2")
        level3 = request.data.get("Level3")
        level4 = request.data.get("Level4")
        price_min = request.data.get("price_min")
        price_max = request.data.get("price_max")
        brand = request.data.get("brand")
        series = request.data.get("series")
        feature_data = request.data.get("feature")

        rs_catalog = RsCatalog.objects.all()
        if level2:
            rs_catalog = rs_catalog.filter(Level2ID=level2)
        if level3:
            rs_catalog = rs_catalog.filter(Level3ID=level3)
        if level4:
            rs_catalog = rs_catalog.filter(Level4ID=level4)
        if not (level4 or level3 or level2):
            return Response({"Error": "GET Level"})

        row_ = Product.objects.filter(id__in=rs_catalog.values_list("product_catalog", flat=True))

        if price_min:
            row_ = row_.filter(RetailPrice__gte=price_min)
        if price_max:
            row_ = row_.filter(RetailPrice__lte=price_max)

        if brand:
            k = chek_list_int(brand)
            if len(k) != 0:
                row_ = row_.filter(brand__in=k)
            else:
                return Response(status.HTTP_204_NO_CONTENT)
        if series:
            k = chek_list_int(series)
            if len(k) != 0:
                row_ = row_.filter(Series__in=k)
            else:
                return Response(status.HTTP_204_NO_CONTENT)

        data = get_object_or_404(FeatureETIMDetails, id=feature)
        data_f = list(FeatureETIMDetails_Data.objects.filter(
            featureETIMDetails_product__id__in=row_.values_list("id", flat=True), featureETIMDetails_id=data.id).
                      values("featureValue").
                      annotate(count=Count('featureValue')).
                      order_by('featureValue', Length("featureValue"), "count").
                      values('featureValue', 'count'))

        if feature_data:
            try:
                feature_data = json.loads(feature_data)
                list_feature_id = [h["feature_id"] for h in feature_data]
                data_g = FeatureETIMDetails.objects.filter(id__in=list_feature_id)

                datas = FeatureETIMDetails_Data.objects.filter(featureETIMDetails__in=data_g.values("id"))
                for h in feature_data:
                    datas = datas.filter(featureValue__in=h["service"])

                datas = datas.values("featureValue"). \
                    order_by('featureValue', Length("featureValue")). \
                    values_list('featureValue', flat=True)

                for i in data_f:
                    if i["featureValue"] not in datas:
                        i["disable"] = True

            except Exception as e:
                return Response({"ERROR": "Feature Example: {'1567': ['300']}", "service": str(e)},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {
                "feature_id": data.id,
                "feature": data.featureName,
                "service": data_f,
            }
        )


class CatalogValues(APIView):
    @staticmethod
    def post(request, limit, page):
        level2 = request.data.get("Level2")
        level3 = request.data.get("Level3")
        level4 = request.data.get("Level4")
        price_min = request.data.get("price_min")
        price_max = request.data.get("price_max")
        sort = request.data.get("sort")
        brand = request.data.get("brand")
        series = request.data.get("series")
        feature = request.data.get("feature")
        update_filters = request.data.get("updateFilters", True)

        rs_catalog = RsCatalog.objects.all()
        if level2:
            rs_catalog = rs_catalog.filter(Level2ID=level2)
        if level3:
            rs_catalog = rs_catalog.filter(Level3ID=level3)
        if level4:
            rs_catalog = rs_catalog.filter(Level4ID=level4)
        if not (level4 or level3 or level2):
            return Response({"Error": "GET Level"})

        row_ = Product.objects.filter(id__in=rs_catalog.values_list("product_catalog", flat=True))
        if price_min:
            row_ = row_.filter(RetailPrice__gte=price_min)
        if price_max:
            row_ = row_.filter(RetailPrice__lte=price_max)

        if brand:
            k = chek_list_int(brand)
            if len(k) != 0:
                row_ = row_.filter(brand__in=k)
            else:
                return Response(status.HTTP_204_NO_CONTENT)
        if series:
            k = chek_list_int(series)
            if len(k) != 0:
                row_ = row_.filter(Series__in=k)
            else:
                return Response(status.HTTP_204_NO_CONTENT)
        if feature:
            try:
                feature = json.loads(feature)
                list_feature_id = [h["feature_id"] for h in feature]
                data = FeatureETIMDetails.objects.filter(id__in=list_feature_id)

                datas = FeatureETIMDetails_Data.objects.filter(featureETIMDetails__in=data.values("id"))
                for h in feature:
                    datas = datas.filter(featureValue__in=h["service"])
                row_ = row_.filter(id__in=datas.values("featureETIMDetails_product_id"))
            except Exception as e:
                return Response({"ERROR": "Feature Example: {'1567': ['300']}", "service": str(e)},
                                status=status.HTTP_400_BAD_REQUEST)
        if sort:
            if sort in ["descending", "ascending", "popularity", "descendingGroup", "ascendingGroup"]:
                if sort == "descending":
                    row_ = row_.order_by("-RetailPrice")
                elif sort == "ascending":
                    row_ = row_.order_by("RetailPrice")
                elif sort == "descendingGroup":
                    row_ = row_.order_by("-ProductName", "RetailPrice")
                elif sort == "ascendingGroup":
                    row_ = row_.order_by("ProductName", "RetailPrice")
                elif sort == "popularity":
                    raw = Order_list.objects.filter(product__in=row_.values("id")).annotate(counts=Sum('count'))
                    row_ = row_.order_by(
                        Subquery(raw.filter(product_id=OuterRef('id')).values('counts')[:1])
                    )
            else:
                return Response({"Error": "Find type error"})

        start_index = (page - 1) * limit
        end_index = start_index + limit

        row_count = row_.count()

        filter_data = []
        filters = {"others": []}
        if update_filters == "1":

            feature_data = FeatureETIMDetails_Data.objects.filter(
                featureETIMDetails_product__id__in=row_.values_list("id"))
            filters["others"] = []
            filters["others"].append({"name": "Brands", "values": Brand.objects.filter(
                id__in=row_.values_list("brand", flat=True)).values("id", "name")})
            filters["others"].append({"name": "Series", "values": Series.objects.filter(
                id__in=row_.values_list("Series", flat=True)).values("id", "name")})

            feature = FeatureETIMDetails.objects.filter(id__in=feature_data.values_list("featureETIMDetails")).values()

            result = (
                feature_data
                .values('featureETIMDetails_id', 'featureValue')
                .annotate(count=Count('featureETIMDetails_id'))
                .order_by('featureETIMDetails_id', Length("featureValue"), 'featureValue')
                .filter(featureValue__isnull=False)
                .values('featureETIMDetails_id', 'featureValue', 'count')
            )

            id_detail = -1
            count_feature = 0
            for i in result:
                if i["featureETIMDetails_id"] != id_detail:
                    if id_detail != -1:
                        h = filters.get(id_detail)
                        h["Count"] = count_feature
                        count_feature = 0

                    id_detail = i["featureETIMDetails_id"]
                    for b, d in enumerate(feature):
                        if d['id'] == i["featureETIMDetails_id"]:
                            count_feature += i["count"]
                            filters[id_detail] = {
                                "featureETIMDetails_id": i["featureETIMDetails_id"],
                                "featureCode": d["featureCode"],
                                "featureName": d["featureName"],
                                "featureUom": d["featureUom"],
                                "Count": i["count"],
                                "featureValue": [{"featureValue": i["featureValue"], "count": i["count"]}]
                            }
                            break
                elif i["featureETIMDetails_id"] == id_detail:
                    count_feature += i["count"]
                    h = filters.get(id_detail)
                    h["featureValue"].append(
                        {"featureValue": i["featureValue"], "count": i["count"]}
                    )

            for i in list(filters.keys())[1:]:
                filter_data.append(filters.get(i))
        return Response({
            "count_pages": math.ceil(row_count / limit),
            "price_min": row_.aggregate(Min('RetailPrice'))["RetailPrice__min"],
            "price_max": row_.aggregate(Max('RetailPrice'))["RetailPrice__max"],
            "service": row_[start_index:end_index].values("id", "is_hit", "is_new", "discount", "Dimension", "EAN",
                                                          "GuaranteePeriod",
                                                          "image", "ItemID", "ItemsPerUnit", "Multiplicity",
                                                          "ParentProdCode", "ParentProdGroup", "ProductCode",
                                                          "ProductDescription", "ProductGroup", "ProductName",
                                                          "SenderPrdCode", "UOM",
                                                          "Weight", "brand", "brand__name", "Series", "Series__name",
                                                          "AnalitCat", "Price2", "RetailPrice", "RetailCurrency", ),
            "others": filters["others"] if update_filters else [],
            "filters": filter_data if update_filters else [],
        })


class OpenProduct(APIView):
    @staticmethod
    def get(request, pk):
        product = get_object_or_404(Product, id=pk)
        country = Country.objects.filter(country_product=pk)
        feature_data = FeatureETIMDetails_Data.objects.filter(featureETIMDetails_product__id=pk)
        feature = FeatureETIMDetails.objects.filter(
            id__in=feature_data.distinct("featureETIMDetails").values_list("featureETIMDetails", flat=True))

        related_prods = RelatedProd.objects.filter(relatedProd_product__id=pk)
        catalog_brochure = CatalogBrochure.objects.filter(brochure_product__id=pk).first()
        rs_catalog = RsCatalog.objects.filter(product_catalog__id=pk).first()
        images = Product_image.objects.filter(image_product__id=pk)
        videos = Product_video.objects.filter(video_product__id=pk)

        certificate_serializer = CertificateInfoSerializer(
            instance=CertificateInfo.objects.filter(certificate_product__id=pk), many=True)

        row = list(feature_data.values())
        row_data = feature.values()

        for i in row:
            for g in row_data:
                if int(i["featureETIMDetails_id"]) == int(g["id"]):
                    i["featureCode"] = g["featureCode"]
                    i["featureUom"] = g["featureUom"]
                    i["featureName"] = g["featureName"]
                    break
        related_prod_serializer = RelatedProdSerializer(instance=related_prods, many=True)
        image_serializer = Product_imageSerializer(instance=images, many=True)
        video_serializer = Product_videoSerializer(instance=videos, many=True)

        data = {
            "product": ProductSerializer(product).data,
            "country": country.values("countries_id__data") if country else [],
            "certificate_info": certificate_serializer.data,
            "related_prod": related_prod_serializer.data,
            "catalog_brochure": CatalogBrochureSerializer(catalog_brochure).data if catalog_brochure else {},
            "rs_catalog": RsCatalogSerializer(rs_catalog).data if rs_catalog else {},
            "images": image_serializer.data,
            "videos": video_serializer.data,
            "feature": row,
        }

        return Response(data)


class UpdatePricat(APIView):
    @staticmethod
    def post(request):
        print("start")
        xml_dict = getfile("service.russvet.ru", "progresselektro", "B8aj17x4", "/pricat/",
                           f"{BASE_DIR}/staticfiles/prodat/")
        data = xml_dict["Document"]["DocDetail"]
        from django.db.models import F

        updated_products = []

        for i in data:
            qty = i["QTY"].replace(".0000", "0")
            sum_qty = i["SumQTY"].replace(".0000", "0")

            if i["RetailPrice"] == 'Цена по запросу':
                retail_price = None
            else:
                retail_price = float(i["RetailPrice"])

            product_kwargs = {
                'AnalitCat': i["AnalitCat"],
                'QTY': qty,
                'SumQTY': float(sum_qty),
                'Price2': float(i["Price2"]),
                'RetailPrice': retail_price,
                'RetailCurrency': i["RetailCurrency"],
                'CustPrice': float(i["CustPrice"]),
            }

            if i["SupOnhandDetail"] is not None:
                dat = datetime.strptime(str(i["SupOnhandDetail"]["LastUpdDate"]), "%Y%m%d")
                product_kwargs.update({
                    'PartnerQTY': float(i["SupOnhandDetail"]["PartnerQTY"]),
                    'PartnerUOM': i["SupOnhandDetail"]["PartnerUOM"],
                    'LastUpdDate': dat,
                })
            product = Product(id=i["ItemId"], **product_kwargs)
            product.QTY = F('QTY')
            product.SumQTY = F('SumQTY')

            updated_products.append(product)
        Product.objects.bulk_update(updated_products,
                                    fields=['AnalitCat', 'QTY', 'SumQTY', 'Price2', 'RetailPrice', 'RetailCurrency',
                                            'CustPrice', 'PartnerQTY', 'PartnerUOM', 'LastUpdDate'])
        return Response("GetAll")


class UpdateCatalog(APIView):
    @staticmethod
    def get(request):
        data = update_catalog()
        with open("catalog.json", "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return Response(data, status=status.HTTP_200_OK)
