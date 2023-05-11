import json
import psycopg2
import requests


def update_products():
    conn = psycopg2.connect(
        host="89.111.136.153",
        database="database_she_2",
        user="postgres",
        password="postgres"
    )
    cursor = conn.cursor()

    cursor.execute("""SELECT ppm.id, ppt.name, ppm.article_moy_sklad from product_product inner join product_product_more ppm on product_product.id = ppm.product_id_id
    inner join product_product_translation ppt on product_product.id = ppt.master_id where ppt.language_code = 'ru' and ppm.article_moy_sklad is not NULL""")

    row = cursor.fetchall()

    data_local = []
    for j in row:
        data_local.append({"id_main": j[0], "name": j[1], "article_moy_sklad": j[2]})
    conn.close()
    print(data_local)
    url = "https://online.moysklad.ru/api/remap/1.2/entity/product?filter=archived=False;pathName=SHE Готовая продукция"

    headers = {
        'Authorization': 'Bearer 99c37d4811522551bb7fff01a87def8c07490b70',
        'Cookie': 'moysklad.firstEntryPoint=https%3A%2F%2Fonline.moysklad.ru%2Flogon; moysklad.reseller=LogneX'
    }

    response = requests.request("GET", url, headers=headers)
    result = json.loads(response.text)

    data_sklad = []
    data = result["rows"]
    for a, i in enumerate(data):
        try:
            data_sklad.append({"id": i["id"], "name": i["name"], "code": i["code"], "volume": i["volume"],
                               "price": i["salePrices"][0]["value"]})
        except:
            pass

    data_sorted = []

    for i in data_local:
        for g in data_sklad:
            try:
                if int(i["article_moy_sklad"]) == int(g["code"]):
                    data_sorted.append({"id": g["id"], "id_main": i["id_main"], "code": g["code"], "name": i["name"],
                                        "name_sklad": g["name"], "volume": int(g["volume"]*100), "price": int(g["price"] / 100)})
            except:
                pass

    url = "https://online.moysklad.ru/api/remap/1.2/report/stock/bystore/current?filter=storeId=15cc2068-f3d4-11ec-0a80-00ce0011107c"

    headers = {
        'Authorization': 'Bearer 99c37d4811522551bb7fff01a87def8c07490b70',
        'Cookie': 'moysklad.firstEntryPoint=https%3A%2F%2Fonline.moysklad.ru%2Flogon; moysklad.reseller=LogneX'
    }

    response = requests.request("GET", url, headers=headers)
    count_products = json.loads(response.text)
    print(count_products)
    for i in data_sorted:
        for h in count_products:
            if h["assortmentId"] == i["id"]:
                i["count"] = h["stock"]

    conn = psycopg2.connect(
        host="89.111.136.153",
        database="database_she_2",
        user="postgres",
        password="postgres"
    )
    cursor = conn.cursor()
    for i in data_sorted:
        try:
            print(i)
            cursor.execute(
                f"UPDATE product_product_more SET price = {i['price']}, availability = {i['count']} where id = {i['id_main']}")
        except Exception as e:
            print(e)
    conn.commit()
    cursor.close()
