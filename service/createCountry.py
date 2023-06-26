from asgiref.sync import sync_to_async


async def create_country(i, main_product_id, connection):
    from product.models import Countries, Country
    if i["Country"] is not None:
        if isinstance(i["Country"]["Value"], list):
            for cont in i["Country"]["Value"]:
                countries, created = await sync_to_async(Countries.objects.using(connection.alias).get_or_create
                                                         )(data=cont)
                await sync_to_async(Country.objects.get_or_create)(
                    country_product_id=main_product_id,
                    countries_id=countries.id
                )
        else:
            countries, created = await sync_to_async(Countries.objects.using(connection.alias).get_or_create
                                                     )(data=i["Country"]["Value"])
            await sync_to_async(Country.objects.get_or_create)(
                country_product_id=main_product_id,
                countries_id=countries.id
            )