
async def create_catalog_brochure(i, main_product_id, connection):
    from product.models import CatalogBrochure
    if i["CatalogBrochure"] is not None:
        if isinstance(i["CatalogBrochure"]["Value"], str):

            await CatalogBrochure.objects.using(connection.alias).aget_or_create(
                brochure_product_id=main_product_id,
                data=i["CatalogBrochure"]["Value"]
            )

        else:
            for h in i["CatalogBrochure"]["Value"]:
                await CatalogBrochure.objects.using(connection.alias).aget_or_create(
                    brochure_product_id=main_product_id,
                    data=h
                )
