

async def process_product_series_brand(i, main_product, connection):
    from product.models import Brand, Series
    brand_main, created = await Brand.objects.using(connection.alias).aget_or_create(name=i["Brand"])
    await brand_main.asave()

    series_main, created = await Series.objects.using(connection.alias).aget_or_create(name=i["Series"])
    await series_main.asave()

    main_product.Series = series_main
    main_product.brand = brand_main
    await main_product.asave()
