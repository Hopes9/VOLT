from product.models import Product, CertificateInfo, CatalogBrochure, RsCatalog, RelatedProd, FeatureETIMDetails_Data, \
    Country, Product_image, Product_video, FeatureETIMDetails

from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "is_hit", "is_new", "discount", "Dimension", "EAN", "GuaranteePeriod",
                  "image", "ItemID", "ItemsPerUnit", "Multiplicity", "ParentProdCode", "ParentProdGroup", "ProductCode",
                  "ProductDescription", "ProductGroup", "ProductName", "SenderPrdCode", "UOM",
                  "Weight", "brand", "Series", "AnalitCat", "Price2", "RetailPrice", "RetailCurrency",
                  ]


class CertificateInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificateInfo
        fields = ["service", ]


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["service", ]


class FeatureETIMDetails_Serializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureETIMDetails
        fields = "__all__"


class FeatureETIMDetails_DataSerializer(serializers.ModelSerializer):
    featureETIMDetails = FeatureETIMDetails_Serializer()

    class Meta:
        model = FeatureETIMDetails_Data
        fields = "__all__"


class FeatureETIMDetailsSerializer(serializers.ModelSerializer):
    featureETIMDetails = FeatureETIMDetails_Serializer()

    class Meta:
        model = FeatureETIMDetails
        fields = "__all__"


class RelatedProdSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedProd
        fields = "__all__"


class CatalogBrochureSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogBrochure
        fields = ["service", ]


class RsCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RsCatalog
        fields = "__all__"


class Product_imageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_image
        fields = "__all__"


class Product_videoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product_video
        fields = ["videoURL", ]
