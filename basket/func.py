def sum_price(basket_items):
    data = list(basket_items)
    total_price = 0
    total_discount = 0

    for item in data:
        if item["buy_now"]:
            if item["product__discount"] is None:
                total_price += item['count'] * item['product__RetailPrice']
            else:
                total_discount += item['count'] * (item['product__Retail'
                                                        'Price'] - item['product__discount'])
                total_price += item['count'] * item['product__discount']
    response = {"total_price": total_price, }
    if total_discount > 0:
        response['total_discount'] = round(total_discount, 1)
    response["service"] = data
    return response
