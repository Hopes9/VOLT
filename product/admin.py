from django.contrib import admin
from django.db import models
from django.forms import Textarea

from .models import Product, Favorite_product, Brand, Passport, Country, Analog, FeatureETIMDetails, RsCatalog, \
    Product_video, Product_image, CatalogBrochure, RelatedProd, CertificateInfo, FeatureETIMDetails_Data, Series


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ["id", "name"]


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ["id", "name"]


@admin.register(Analog)
class AnalogAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'analog_product')
    list_display = ["id", "analog_product"]


admin.site.register(Passport, admin.ModelAdmin)

admin.site.register(Country, admin.ModelAdmin)

admin.site.register(CertificateInfo, admin.ModelAdmin)
admin.site.register(RelatedProd, admin.ModelAdmin)
admin.site.register(CatalogBrochure, admin.ModelAdmin)

admin.site.register(Product_image, admin.ModelAdmin)
admin.site.register(Product_video, admin.ModelAdmin)
admin.site.register(Favorite_product, admin.ModelAdmin)


@admin.register(RsCatalog)
class RsCatalogAdmin(admin.ModelAdmin):
    readonly_fields = ('product_catalog',)
    list_display = ["id", "product_catalog", "Level2ID", "Level2Name", "Level3ID", "Level3Name", "Level4ID",
                    "Level4Name"]


@admin.register(FeatureETIMDetails)
class FeatureETIMDetailsAdmin(admin.ModelAdmin):
    readonly_fields = ()
    list_display = [
        "id",
        "featureCode",
        "featureUom",
        "featureName",
    ]
    list_max_show_all = 5000000
    list_per_page = 1000


@admin.register(FeatureETIMDetails_Data)
class FeatureETIMDetailsDataAdmin(admin.ModelAdmin):
    readonly_fields = ("featureETIMDetails_product", "featureETIMDetails")
    list_display = [
        "id",
        "featureETIMDetails_product",
        "featureETIMDetails",
        "featureValue",
    ]
    list_max_show_all = 5000000
    list_per_page = 1000


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'brand', 'Series',)
    list_display = ["ProductName", "RetailPrice", "is_hit", "is_new", ]
    list_max_show_all = 30000
    list_per_page = 1000
    search_help_text = True


class Product_AdminInline(admin.TabularInline):
    show_change_link = True
    model = Product
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 20})},
    }

# from django.shortcuts import redirect
#
#
# def run_task(request):
#     update_products()
#     return redirect('admin:index')
