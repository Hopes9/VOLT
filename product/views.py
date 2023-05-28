import json
import json
import mmap
from collections import Counter
from pprint import pprint

import xmltodict
from django.db import connection
from django.db.models import Q, Max, Min, Count, Sum, Subquery, OuterRef
from django.db.models.functions import Length
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from order.models import Order, Order_list
from product.func import update_catalog, chekListInt, percent
from product.models import Product, Analog, Brand, CatalogBrochure, CertificateInfo, Country, FeatureETIMDetails, \
    FeatureETIMDetails_Data, Product_image, Passport, RelatedProd, RsCatalog, Product_video, Series
from product.serializers import ProductSerializer, CertificateInfoSerializer, Product_imageSerializer, \
    Product_videoSerializer, RelatedProdSerializer, CountrySerializer, \
    RsCatalogSerializer, CatalogBrochureSerializer, FeatureETIMDetails_DataSerializer


class Product_(APIView):
    def get(self, request):
        offset = 0
        limit = 30
        if request.data.get("offset") is not None:
            offset = int(request.data.get("offset"))

        if request.data.get("limit") is not None:
            limit = int(request.data.get("limit"))

        products = Product.objects.order_by('id')[offset:limit]  # offset 9, limit 30
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class Search_product(APIView):
    def post(self, request):
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


class catalog(APIView):
    def get(self, request):
        with open("catalog.json", "r", encoding="UTF-8") as f:
            data = f.read()
        data = json.loads(data)
        return Response(data, status=status.HTTP_200_OK)


class getFilters(APIView):
    def post(self, request):
        Level2 = request.data.get("Level2")
        Level3 = request.data.get("Level3")
        Level4 = request.data.get("Level4")
        price_min = request.data.get("price_min")
        price_max = request.data.get("price_max")
        brand = request.data.get("brand")
        series = request.data.get("series")
        feature = request.data.get("feature")

        rsCatalog = RsCatalog.objects.all()
        if Level2:
            rsCatalog = rsCatalog.filter(Level2ID=Level2)
        if Level3:
            rsCatalog = rsCatalog.filter(Level3ID=Level3)
        if Level4:
            rsCatalog = rsCatalog.filter(Level4ID=Level4)
        if not (Level4 or Level3 or Level2):
            return Response({"Error": "GET Level"})

        row_ = Product.objects.filter(id__in=rsCatalog.values_list("product_catalog", flat=True))
        if price_min:
            row_ = row_.filter(RetailPrice__gte=price_min)
        if price_max:
            row_ = row_.filter(RetailPrice__lte=price_max)

        if brand:
            k = chekListInt(brand)
            if len(k) != 0:
                row_ = row_.filter(brand__in=k)
            else:
                return Response(status.HTTP_204_NO_CONTENT)
        if series:
            k = chekListInt(series)
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
                    datas = datas.filter(featureValue__in=h["data"])
                row_ = row_.filter(id__in=datas.values("featureETIMDetails_product_id"))
            except Exception as e:
                return Response({"ERROR": "Feature Example: {'1567': ['300']}", "data": str(e)},
                                status=status.HTTP_400_BAD_REQUEST)
        filters["filters"] = FeatureETIMDetails.objects.filter(featureetimdetails_data__featureETIMDetails_product__id__in=
                                                               row_.values_list("id", flat=True)).distinct("featureName").values()

        filters["others"] = [{"name": "Brands",
                              "values": Brand.objects.filter(id__in=row_.values_list("brand", flat=True)).values(
                                  "id", "name")},
                             {"name": "Series",
                              "values": Series.objects.filter(id__in=row_.values_list("Series", flat=True)).values(
                                  "id", "name")}]

        return Response(filters)


class getFiltersInt(APIView):
    def post(self, request, feature):
        Level2 = request.data.get("Level2")
        Level3 = request.data.get("Level3")
        Level4 = request.data.get("Level4")
        price_min = request.data.get("price_min")
        price_max = request.data.get("price_max")
        brand = request.data.get("brand")
        series = request.data.get("series")

        rsCatalog = RsCatalog.objects.all()
        if Level2:
            rsCatalog = rsCatalog.filter(Level2ID=Level2)
        if Level3:
            rsCatalog = rsCatalog.filter(Level3ID=Level3)
        if Level4:
            rsCatalog = rsCatalog.filter(Level4ID=Level4)
        if not (Level4 or Level3 or Level2):
            return Response({"Error": "GET Level"})

        row_ = Product.objects.filter(id__in=rsCatalog.values_list("product_catalog", flat=True))

        if price_min:
            row_ = row_.filter(RetailPrice__gte=price_min)
        if price_max:
            row_ = row_.filter(RetailPrice__lte=price_max)

        if brand:
            k = chekListInt(brand)
            if len(k) != 0:
                row_ = row_.filter(brand__in=k)
            else:
                return Response(status.HTTP_204_NO_CONTENT)
        if series:
            k = chekListInt(series)
            if len(k) != 0:
                row_ = row_.filter(Series__in=k)
            else:
                return Response(status.HTTP_204_NO_CONTENT)

        data = FeatureETIMDetails.objects.get(id=feature)
        dataF = FeatureETIMDetails_Data.objects.filter(featureETIMDetails_product__id__in=row_.values_list("id", flat=True), featureETIMDetails_id=data.id)
        return Response(
            {
                "feature_id": data.id,
                "feature": data.featureName,
                "data": dataF.values("featureValue").annotate(count=Count('featureValue')).order_by("-count")
                .order_by('featureValue', Length("featureValue"), "count")
                .values('featureValue', 'count')
            }
        )


class catalog_values(APIView):
    def post(self, request, limit, page):
        Level2 = request.data.get("Level2")
        Level3 = request.data.get("Level3")
        Level4 = request.data.get("Level4")
        price_min = request.data.get("price_min")
        price_max = request.data.get("price_max")
        sort = request.data.get("sort")
        brand = request.data.get("brand")
        series = request.data.get("series")
        feature = request.data.get("feature")
        updateFilters = request.data.get("updateFilters", True)

        rsCatalog = RsCatalog.objects.all()
        if Level2:
            rsCatalog = rsCatalog.filter(Level2ID=Level2)
        if Level3:
            rsCatalog = rsCatalog.filter(Level3ID=Level3)
        if Level4:
            rsCatalog = rsCatalog.filter(Level4ID=Level4)
        if not (Level4 or Level3 or Level2):
            return Response({"Error": "GET Level"})

        row_ = Product.objects.filter(id__in=rsCatalog.values_list("product_catalog", flat=True))
        if price_min:
            row_ = row_.filter(RetailPrice__gte=price_min)
        if price_max:
            row_ = row_.filter(RetailPrice__lte=price_max)

        if brand:
            k = chekListInt(brand)
            if len(k) != 0:
                row_ = row_.filter(brand__in=k)
            else:
                return Response(status.HTTP_204_NO_CONTENT)
        if series:
            k = chekListInt(series)
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
                    datas = datas.filter(featureValue__in=h["data"])
                row_ = row_.filter(id__in=datas.values("featureETIMDetails_product_id"))
            except Exception as e:
                return Response({"ERROR": "Feature Example: {'1567': ['300']}", "data": str(e)},
                                status=status.HTTP_400_BAD_REQUEST)
        if sort:
            if sort in ["descending", "ascending", "popularity"]:
                if sort == "descending":
                    row_ = row_.order_by("-ProductName")
                elif sort == "ascending":
                    row_ = row_.order_by("ProductName")
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
        if updateFilters == "1":

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
            countFeature = 0
            for i in result:
                if i["featureETIMDetails_id"] != id_detail:
                    if id_detail != -1:
                        h = filters.get(id_detail)
                        h["Count"] = countFeature
                        countFeature = 0

                    id_detail = i["featureETIMDetails_id"]
                    for b, d in enumerate(feature):
                        if d['id'] == i["featureETIMDetails_id"]:
                            countFeature += i["count"]
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
                    countFeature += i["count"]
                    h = filters.get(id_detail)
                    h["featureValue"].append(
                        {"featureValue": i["featureValue"], "count": i["count"]}
                    )

            for i in list(filters.keys())[1:]:
                filter_data.append(filters.get(i))
        return Response({
            "count_pages": row_count // limit,
            "price_min": row_.aggregate(Min('RetailPrice'))["RetailPrice__min"],
            "price_max": row_.aggregate(Max('RetailPrice'))["RetailPrice__max"],
            "data": row_[start_index:end_index].values("id", "is_hit", "is_new", "discount", "Dimension", "EAN",
                                                       "GuaranteePeriod",
                                                       "image", "ItemID", "ItemsPerUnit", "Multiplicity",
                                                       "ParentProdCode", "ParentProdGroup", "ProductCode",
                                                       "ProductDescription", "ProductGroup", "ProductName",
                                                       "SenderPrdCode", "UOM",
                                                       "Weight", "brand", "brand__name", "Series", "Series__name",
                                                       "AnalitCat", "Price2", "RetailPrice", "RetailCurrency", ),
            "others": filters["others"] if updateFilters else [],
            "filters": filter_data if updateFilters else [],
        })


class Open_product(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        country = Country.objects.filter(country_product__id=pk)
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
            "country": CountrySerializer(instance=country, many=True).data if country else [],
            "certificate_infos": certificate_serializer.data,
            "related_prods": related_prod_serializer.data,
            "catalog_brochure": CatalogBrochureSerializer(catalog_brochure).data if catalog_brochure else {},
            "rs_catalog": RsCatalogSerializer(rs_catalog).data if rs_catalog else {},
            "images": image_serializer.data,
            "videos": video_serializer.data,
            "feature": row,
        }

        return Response(data)


@permission_classes([IsAuthenticated])
class Update_pricat(APIView):
    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response(status=status.HTTP_204_NO_CONTENT)

        with open('staticfiles/prodat/pricat.xml', "wb+") as f:
            for chunk in file.chunks():
                f.write(chunk)

        with open('staticfiles/prodat/pricat.xml', "rb") as f:
            mapped_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            xml_string = mapped_file.read()
            mapped_file.close()

        xml_dict = xmltodict.parse(xml_string)
        data = xml_dict["Document"]["DocDetail"]

        count = 0

        for i in data:
            print(count)
            count += 1
            QTY = i["QTY"].replace(".0000", "0")
            SumQTY = i["SumQTY"].replace(".0000", "0")
            if i["RetailPrice"] == 'Цена по запросу':
                RetailPrice = None
            else:
                RetailPrice = float(i["RetailPrice"])

            try:
                Product.objects.filter(ItemID=i["ItemId"]).update(
                    AnalitCat=i["AnalitCat"],
                    QTY=QTY,
                    SumQTY=float(SumQTY),
                    Price2=float(i["Price2"]),
                    RetailPrice=RetailPrice,
                    RetailCurrency=i["RetailCurrency"],
                    CustPrice=float(i["CustPrice"]),
                    MRC=float(i["MRC"]),
                )
            except Exception as e:
                print(i)
                print(e)
                break
        return Response(data, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class UpdateCatalog(APIView):
    def get(self, request):
        data = update_catalog()
        with open("catalog.json", "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return Response(data, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
class Update_prodat(APIView):
    def post(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response(status=status.HTTP_204_NO_CONTENT)

        with open('staticfiles/prodat/prodat.xml', "wb+") as f:
            for chunk in file.chunks():
                f.write(chunk)

        with open('staticfiles/prodat/prodat.xml', "rb") as f:
            mapped_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            xml_string = mapped_file.read()
            mapped_file.close()

        xml_dict = xmltodict.parse(xml_string)
        data = xml_dict["Document"]["DocDetail"]
        print(0, len(data))
        count = 0
        try:
            for i in data:
                print(count)
                try:
                    if i["EAN"] is not None:
                        EAN = i["EAN"]["Value"]
                    else:
                        EAN = None

                    Main_product, created = Product.objects.update_or_create(ItemID=i["ItemID"], defaults={
                        "Dimension": i["Dimension"],
                        "EAN": EAN,
                        "GuaranteePeriod": i["GuaranteePeriod"],
                        "ItemsPerUnit": i["ItemsPerUnit"],
                        "Multiplicity": i["Multiplicity"],
                        "ParentProdCode": i["ParentProdCode"],
                        "ParentProdGroup": i["ParentProdGroup"],
                        "ProductCode": i["ProductCode"],
                        "ProductDescription": i["ProductDescription"],
                        "ProductGroup": i["ProductGroup"],
                        "ProductName": i["ProductName"],
                        "SenderPrdCode": i["SenderPrdCode"],
                        "UOM": i["UOM"],
                        "VendorProdNum": i["VendorProdNum"],
                        "Weight": i["Weight"]["Value"]
                    }
                    )
                    Main_product.save()
                    MId = Main_product.id
                except Exception as e:
                    print(i)
                    print(e, "1")
                    break
                try:
                    if i["Analog"] is not None:
                        if type(i["Analog"]) is dict:
                            Analog_main, created = Analog.objects.update_or_create(analog_product_id=MId,
                                                                                   data=i["Analog"]["ItemCode"])
                            Analog_main.save()
                        else:
                            for g in i["Analog"]["ItemCode"]:
                                Analog_main, created = Analog.objects.update_or_create(analog_product_id=MId,
                                                                                       data=g)
                                Analog_main.save()

                    Brand_main, created = Brand.objects.get_or_create(name=i["Brand"])
                    Brand_main.save()
                    Series_main, created = Series.objects.get_or_create(name=i["Series"])
                    Series_main.save()
                    Main_product.Series_id = Series_main.id
                    Main_product.brand_id = Brand_main.id
                    Main_product.save()
                except Exception as e:
                    print(i)
                    print(e, "2")
                    break
                try:
                    if i["CatalogBrochure"] is not None:
                        for h in i["CatalogBrochure"]["Value"]:
                            CatalogBrochure_main, created = CatalogBrochure.objects.update_or_create(
                                brochure_product_id=MId, data=h)
                            CatalogBrochure_main.save()
                except Exception as e:
                    print(i)
                    print(e, "3")
                    break
                try:
                    if i["CertificateInfo"] is not None:
                        if type(i["CertificateInfo"]["Certificate"]) is dict:
                            CertificateInfo_main, created = CertificateInfo.objects.update_or_create(
                                certificate_product_id=MId,
                                data=i["CertificateInfo"]["Certificate"]["CertificateURL"])
                            CertificateInfo_main.save()
                        else:
                            for j in i["CertificateInfo"]["Certificate"]:
                                CertificateInfo_main, created = CertificateInfo.objects.update_or_create(
                                    certificate_product_id=MId, data=j["CertificateURL"])
                                CertificateInfo_main.save()
                except Exception as e:
                    print(i)
                    print(e, "4")
                    break
                try:
                    if i["Country"] is not None:
                        if type(i["Country"]) is dict:
                            Country_main, created = Country.objects.update_or_create(country_product_id=MId,
                                                                                     data=i["Country"]["Value"])
                            Country_main.save()
                        else:
                            for v in i["Country"]:
                                Country_main, created = Country.objects.update_or_create(country_product_id=MId,
                                                                                         data=v["Value"])
                                Country_main.save()
                except Exception as e:
                    print(i)
                    print(e, "5")
                    break
                try:

                    if i["FeatureETIMDetails"] is not None:
                        if type(i["FeatureETIMDetails"]["FeatureETIM"]) is not dict:
                            for k in i["FeatureETIMDetails"]["FeatureETIM"]:
                                if k["FeatureValue"] is not None:
                                    FeatureETIMDetails_main, created = FeatureETIMDetails.objects.update_or_create(
                                        featureCode=k["FeatureCode"],
                                        defaults=dict(
                                            featureName=k["FeatureName"],
                                            featureUom=k["FeatureUom"]
                                        )
                                    )
                                    FeatureETIMDetails_main.save()
                                    FeatureETIMDetails_Data_main, created = FeatureETIMDetails_Data.objects.update_or_create(
                                        featureETIMDetails_product_id=MId,
                                        featureValue=k["FeatureValue"],
                                        featureETIMDetails_id=FeatureETIMDetails_main.id
                                    )
                                    FeatureETIMDetails_Data_main.save()
                        else:
                            if i["FeatureETIMDetails"]["FeatureETIM"]["FeatureValue"] is not None:
                                FeatureETIMDetails_main, created = FeatureETIMDetails.objects.update_or_create(
                                    featureCode=i["FeatureETIMDetails"]["FeatureETIM"]["FeatureCode"],
                                    defaults= dict(
                                        featureName=i["FeatureETIMDetails"]["FeatureETIM"]["FeatureName"],
                                        featureUom=i["FeatureETIMDetails"]["FeatureETIM"]["FeatureUom"]
                                    ),
                                )
                                FeatureETIMDetails_main.save()
                                FeatureETIMDetails_Data_main, created = FeatureETIMDetails_Data.objects.update_or_create(
                                    featureETIMDetails_product_id=MId,
                                    featureValue=i["FeatureETIMDetails"]["FeatureETIM"]["FeatureValue"],
                                    featureETIMDetails_id=FeatureETIMDetails_main.id)
                                FeatureETIMDetails_Data_main.save()
                except Exception as e:
                    print(i)
                    print(e, "6")
                    break
                try:
                    if i["Image"] is not None:
                        if type(i["Image"]["Value"]) is list:
                            Main_product.image = i["Image"]["Value"][0]
                            Main_product.save()
                            for v in i["Image"]["Value"][1:]:
                                Product_image_main, created = Product_image.objects.update_or_create(
                                    image_product_id=MId, imageURL=v)
                                Product_image_main.save()
                        else:
                            Main_product.image = i["Image"]["Value"]
                            Main_product.save()

                except Exception as e:
                    print(i)
                    print(e, "7")
                    break
                try:
                    if i["Passport"] is not None:
                        if type(i["Passport"]) is dict:
                            Passport_main, created = Passport.objects.update_or_create(passport_product_id=MId,
                                                                                       data=i["Passport"]["Value"])
                            Passport_main.save()
                        else:
                            for v in i["Passport"]:
                                Passport_main, created = Passport.objects.update_or_create(passport_product_id=MId,
                                                                                           data=v["Value"])
                                Passport_main.save()
                except Exception as e:
                    print(i)
                    print(e, "8")
                    break
                try:
                    if i["RelatedProd"] is not None:
                        for u in i["RelatedProd"]["ItemCode"]:
                            RelatedProd_main, created = RelatedProd.objects.update_or_create(relatedProd_product_id=MId,
                                                                                             data=u)
                            RelatedProd_main.save()
                except Exception as e:
                    print(i)
                    print(e, "9")
                    break
                try:
                    if i["RsCatalog"] is not None:
                        RsCatalog_main, created = RsCatalog.objects.update_or_create(product_catalog_id=MId,
                                                                                     Level2ID=i["RsCatalog"][
                                                                                         "Level2ID"],
                                                                                     Level2Name=i["RsCatalog"][
                                                                                         "Level2Name"],
                                                                                     Level3ID=i["RsCatalog"][
                                                                                         "Level3ID"],
                                                                                     Level3Name=i["RsCatalog"][
                                                                                         "Level3Name"],
                                                                                     Level4ID=i["RsCatalog"][
                                                                                         "Level4ID"],
                                                                                     Level4Name=i["RsCatalog"][
                                                                                         "Level4Name"], )
                        RsCatalog_main.save()
                except Exception as e:
                    print(i)
                    print(e, "10")
                    break
                try:
                    if i["Video"] is not None:
                        if type(i["Video"]["Value"]) is list:
                            for v in i["Video"]["Value"]:
                                Product_video_main, created = Product_video.objects.update_or_create(
                                    video_product_id=MId, videoURL=v)
                                Product_video_main.save()
                        else:
                            Product_video_main, created = Product_video.objects.update_or_create(video_product_id=MId,
                                                                                                 videoURL=i["Video"][
                                                                                                     "Value"])
                            Product_video_main.save()
                except Exception as e:
                    print(i)
                    print(e, "11")
                    break
                count += 1
        except Exception as e:
            print(e, "12")
        ##################
        return Response("")
