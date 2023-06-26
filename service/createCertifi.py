
async def create_certificate_info(i, main_product_id, connection):
    from product.models import CertificateInfo
    if i["CertificateInfo"] is not None:
        if isinstance(i["CertificateInfo"]["Certificate"], dict):
            if str(i["CertificateInfo"]["Certificate"]["CertificateURL"]) != "1":
                await CertificateInfo.objects.using(connection.alias).aget_or_create(
                    certificate_product_id=main_product_id,
                    data=i["CertificateInfo"]["Certificate"]["CertificateURL"]
                )
        else:
            for j in i["CertificateInfo"]["Certificate"]:
                if str(j["CertificateURL"]) != "1":
                    
                    await CertificateInfo.objects.using(connection.alias).aget_or_create(
                        certificate_product_id=main_product_id,
                        data=j["CertificateURL"]
                    )
