from asgiref.sync import sync_to_async


async def update_or_create_analog(i, main_product_id, connection):
    from product.models import Analog
    if i["Analog"] is not None:
        if isinstance(i["Analog"], dict):

            await sync_to_async(Analog.objects.using(connection.alias).get_or_create)(
                analog_product_id=main_product_id,
                data=i["Analog"]["ItemCode"]
            )
            
        else:
            for g in i["Analog"]["ItemCode"]:
                await sync_to_async(Analog.objects.using(connection.alias).get_or_create)(
                    analog_product_id=main_product_id,
                    data=g
                )
