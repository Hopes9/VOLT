
async def create_others(i, main_product, connection, main_product_id):
    from product.models import Product_image, Product_video, RsCatalog
    if i["Image"] is not None:
        if isinstance(i["Image"]["Value"], list):
            main_product.image = i["Image"]["Value"][0]
            for v in i["Image"]["Value"][1:]:
                await Product_image.objects.using(connection.alias).aget_or_create(
                    image_product_id=main_product_id,
                    imageURL=v
                )
        else:
            main_product.image = i["Image"]["Value"]
    if i["RsCatalog"] is not None:
        await RsCatalog.objects.using(connection.alias).aget_or_create(
            product_catalog_id=main_product_id,
            Level2ID=i["RsCatalog"]["Level2ID"],
            Level2Name=i["RsCatalog"]["Level2Name"],
            Level3ID=i["RsCatalog"]["Level3ID"],
            Level3Name=i["RsCatalog"]["Level3Name"],
            Level4ID=i["RsCatalog"]["Level4ID"],
            Level4Name=i["RsCatalog"]["Level4Name"]
        )

    if i["Video"] is not None:
        if isinstance(i["Video"]["Value"], list):
            for v in i["Video"]["Value"]:
                await Product_video.objects.using(connection.alias).aget_or_create(
                    video_product_id=main_product_id,
                    videoURL=v
                )
        else:
            await Product_video.objects.using(connection.alias).aget_or_create(
                video_product_id=main_product_id,
                videoURL=i["Video"]["Value"]
            )
