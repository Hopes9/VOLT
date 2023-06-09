from __future__ import unicode_literals

from django.db import IntegrityError, models
from django.utils.translation import gettext_lazy as _


class Brand(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True, db_index=True)
    name = models.TextField(blank=True)

    def __unicode__(self):
        return str(self.name)

    def __str__(self):
        return f'{self.name}'


class Series(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True, db_index=True)
    name = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return str(self.name)

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True, db_index=True)
    is_hit = models.BooleanField(_("Хит!"), null=True, default=False)
    is_new = models.BooleanField(_("Новое!"), null=True, default=False)
    show = models.BooleanField(_("Показывать на сайте"), default=True, blank=True)
    discount = models.IntegerField(_("Скидка цена"), null=True, default=None, blank=True)
    delete = models.BooleanField(default=False)

    Dimension = models.JSONField(_("Единица измерения"), null=True, blank=True)
    EAN = models.JSONField(_("EAN товара (Штрих-код)"), null=True, blank=True)
    GuaranteePeriod = models.TextField(_("Гарантийный срок"), null=True)
    image = models.TextField(_("Фото (Основное)"), null=True, blank=True)
    ItemID = models.BigIntegerField(_("ID позиции"), blank=True, unique=True)
    ItemsPerUnit = models.BigIntegerField(_("Кол-во штук в упаковке"), blank=True, null=True)
    Multiplicity = models.BigIntegerField(_("Кратность закупки у поставщика"), blank=True, null=True)
    ParentProdCode = models.CharField(_("ID категории товара"), max_length=50, blank=True, null=True)
    ParentProdGroup = models.TextField(_("Название категории товара"), blank=True, null=True)
    ProductCode = models.TextField(_("ProductCode"), blank=True, null=True)
    ProductDescription = models.TextField(_("ProductDescription"), blank=True, null=True)
    ProductGroup = models.TextField(_("Товарная группа (Категория каталога)"), null=True, blank=True)
    ProductName = models.TextField(_("ProductName"), null=True, blank=True)
    # ReceiverPrdCode    = models.TextField(_("ReceiverPrdCode"),null=True, blank=True)
    SenderPrdCode = models.BigIntegerField(_("Код товара в УС отправителя"), blank=True, null=True)
    UOM = models.CharField(_("UOM"), max_length=3, blank=True, null=True)
    VendorProdNum = models.TextField(_("Артикул"), null=True, blank=True)
    Weight = models.FloatField(_("Вес"), null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    Series = models.ForeignKey(Series, on_delete=models.CASCADE, blank=True, null=True)

    AnalitCat = models.CharField(_("Аналитическая категория"), max_length=3, blank=True, null=True)
    QTY = models.FloatField(_("Количество"), blank=True, null=True)
    SumQTY = models.FloatField(_("Сумма ост. на складе РС и складе поставщика"), blank=True, null=True)
    Price2 = models.FloatField(_("Цена клиента с НДС"), blank=True, null=True)
    RetailPrice = models.FloatField(_("Базовая цена товара с НДС"), blank=True, null=True)
    RetailCurrency = models.TextField(_("Рекомендованная валюта"), blank=True, null=True)
    CustPrice = models.FloatField(_("Цена клиента без НДС "), blank=True, null=True)
    # MRC                = models.FloatField(_("Артикул"), blank=True, null=True)
    PartnerQTY = models.BigIntegerField(_("Остатки товара"), blank=True, null=True)
    PartnerUOM = models.TextField(_("Единица измерения товара в учетной системе поставщика"), blank=True, null=True)
    LastUpdDate = models.DateField(_("Последнее обновление"), blank=True, null=True, )

    def __unicode__(self):
        return str(self.ProductName)

    def __str__(self):
        return f'{self.VendorProdNum}'


# Паспорт
class Passport(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True, db_index=True)
    passport_product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    data = models.TextField(_("Passport"))


# Аналог
class Analog(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True, db_index=True)
    analog_product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    data = models.TextField(_("Код замены позиции в кодах Русского Света"), )


class Countries(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True, db_index=True)
    data = models.TextField(_("страна производитель"), )


# Страна
class Country(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True, db_index=True)
    country_product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    countries = models.ForeignKey(Countries, on_delete=models.CASCADE, blank=True, null=True)


# Технические характеристики в формате ETIM
class FeatureETIMDetails(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True, db_index=True)
    featureCode = models.TextField(_("Код ETIM"), db_index=True)
    featureUom = models.TextField(_("ЕИ характеристики ETIM"), null=True, blank=True)
    featureName = models.TextField(_("Наименование характеристики ETIM"), null=True, blank=True)


class FeatureETIMDetails_Data(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True, db_index=True)
    featureETIMDetails_product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    featureETIMDetails = models.ForeignKey(FeatureETIMDetails, on_delete=models.CASCADE, blank=True, null=True)
    featureValue = models.TextField(_("Значение характеристики ETIM"), blank=True, null=True)

    class Meta:
        unique_together = (
            ('featureETIMDetails_product', 'featureETIMDetails', 'featureValue'),
        )
        
    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)
        except IntegrityError:
            print('pass')
            pass


# URL сертификат
class CertificateInfo(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True, db_index=True)
    certificate_product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    data = models.TextField(_("URL сертификата сертификата"), blank=True)


# Сопутствующие товары в кодах Русского Света
class RelatedProd(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True, db_index=True)
    relatedProd_product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    data = models.TextField(_("ID сопутствующего товаров"), )


class CatalogBrochure(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True, db_index=True)
    brochure_product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    data = models.TextField(_("ссылка"), )


class RsCatalog(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True, db_index=True)
    product_catalog = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    Level2ID = models.BigIntegerField(_("ID второго уровня РС каталога "), blank=True)
    Level2Name = models.TextField(_("Описание второго уровня РС каталога"), blank=True)
    Level3ID = models.BigIntegerField(_("ID третьего уровня РС каталога"), blank=True, null=True)
    Level3Name = models.TextField(_("Описание третьего уровня РС каталога"), blank=True, null=True)
    Level4ID = models.BigIntegerField(_("ID четвертого уровня РС каталога"), blank=True, null=True)
    Level4Name = models.TextField(_("Описание четвертого уровня РС каталога"), blank=True, null=True)


class Product_image(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True, db_index=True)
    image = models.ImageField(upload_to="staticfiles/img/product", null=True, blank=True)
    imageURL = models.TextField(null=True, blank=True)
    image_product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    show = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return str(self.image)

    def __unicode__(self):
        return self.id


class Product_video(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True, db_index=True)
    videoURL = models.TextField(null=True, blank=True)
    video_product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.videoURL)

    def __unicode__(self):
        return self.id


class Favorite_product(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return str(self.product)
