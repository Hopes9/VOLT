from asgiref.sync import sync_to_async

feature_etim_details_data_objects = []


async def create_feature_etim_details(i, main_product_id, connection):
    from product.models import FeatureETIMDetails, FeatureETIMDetails_Data

    if i["FeatureETIMDetails"] is not None:
        if type(i["FeatureETIMDetails"]["FeatureETIM"]) is not dict:
            for k in i["FeatureETIMDetails"]["FeatureETIM"]:
                if k["FeatureValue"] is not None:
                    feature_etim_details_main, created = await sync_to_async(
                        FeatureETIMDetails.objects.using(connection.alias).update_or_create)(
                        featureCode=k["FeatureCode"],
                        featureName=k["FeatureName"],
                        featureUom=k["FeatureUom"]
                    )
                    feature_etim_details_data_objects.append(FeatureETIMDetails_Data(
                        featureETIMDetails_product_id=main_product_id,
                        featureETIMDetails=feature_etim_details_main,
                        featureValue=k["FeatureValue"]

                    )
                    )
        else:
            if i["FeatureETIMDetails"]["FeatureETIM"]["FeatureValue"] is not None:
                feature_etim_details_main, created = await sync_to_async(
                    FeatureETIMDetails.objects.using(connection.alias).update_or_create)(
                    featureCode=i["FeatureETIMDetails"]["FeatureETIM"]["FeatureCode"],
                    featureName=i["FeatureETIMDetails"]["FeatureETIM"]["FeatureName"],
                    featureUom=i["FeatureETIMDetails"]["FeatureETIM"]["FeatureUom"]
                )

                feature_etim_details_data_objects.append(FeatureETIMDetails_Data(
                    featureETIMDetails_product_id=main_product_id,
                    featureValue=i["FeatureETIMDetails"]["FeatureETIM"]["FeatureValue"],
                    featureETIMDetails_id=feature_etim_details_main.id
                ))
