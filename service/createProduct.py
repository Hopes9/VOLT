from product.models import Product


def update_or_create_product(i):
    if i["EAN"] is not None:
        ean = i["EAN"]["Value"]
    else:
        ean = None
    
    main_product, update = Product.objects.update_or_create(
        ItemID=int(i["ItemID"]),
        defaults={
            "Dimension": i["Dimension"],
            "EAN": ean,
            "GuaranteePeriod": i["GuaranteePeriod"],
            "ItemsPerUnit": i["ItemsPerUnit"],
            "Multiplicity": i["Multiplicity"],
            "ParentProdGroup": i["ParentProdGroup"],
            "ProductCode": i["ProductCode"],
            "ProductDescription": i["ProductDescription"],
            "ProductGroup": i["ProductGroup"],
            "ProductName": i["ProductName"],
            "SenderPrdCode": i["SenderPrdCode"],
            "UOM": i["UOM"],
            "VendorProdNum": i["VendorProdNum"],
            "Weight": i["Weight"]["Value"]
        }
    )
    main_product_id = main_product.id
    return main_product, main_product_id 
