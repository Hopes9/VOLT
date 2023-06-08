import random
import string


def update():

    with open('staticfiles/prodat/pricat.xml', "wb+") as f:
        for chunk in file.chunks():
            f.write(chunk)

    with open('staticfiles/prodat/pricat.xml', "rb") as f:
        import mmap
        mapped_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        xml_string = mapped_file.read()
        mapped_file.close()

    import xmltodict
    xml_dict = xmltodict.parse(xml_string)
    data = xml_dict["Document"]["DocDetail"]

    count = 0

    for i in data:
        print(count)
        count += 1
        QTY = i["QTY"].replace(".0000", "0")
        SumQTY = i["SumQTY"].replace(".0000", "0")
        if i["RetailPrice"] == 'Цена по запросу':
            RetailPrice = None
        else:
            RetailPrice = float(i["RetailPrice"])

        try:
            from product.models import Product
            Product.objects.filter(ItemID=i["ItemId"]).update(
                AnalitCat=i["AnalitCat"],
                QTY=QTY,
                SumQTY=float(SumQTY),
                Price2=float(i["Price2"]),
                RetailPrice=RetailPrice,
                RetailCurrency=i["RetailCurrency"],
                CustPrice=float(i["CustPrice"]),
                MRC=float(i["MRC"]),
            )
        except Exception as e:
            print(i)
            print(e)
            break


def start_scheduler(*args, **kwargs):
    from apscheduler.jobstores.memory import MemoryJobStore
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.interval import IntervalTrigger

    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(MemoryJobStore(), "default")

    scheduler.add_job(
        update,
        IntervalTrigger(days=1),
        id="update",
        name="Update",
        replace_existing=True,
    )
    scheduler.start()
