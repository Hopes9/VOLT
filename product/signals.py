from datetime import datetime

import pytz
from apscheduler.triggers.cron import CronTrigger

from VOLT import settings
from VOLT.settings import BASE_DIR
from product.ftp import getfile
from service.main import clear_directory, start_prodat


def update():
    xml_dict = getfile("service.russvet.ru", "progresselektro", "B8aj17x4", "/pricat/",
                       f"{BASE_DIR}/staticfiles/prodat/")
    data = xml_dict["Document"]["DocDetail"]

    count = 0

    for i in data:
        print(count)
        count += 1
        qty = i["QTY"].replace(".0000", "0")
        sum_qty = i["SumQTY"].replace(".0000", "0")
        if i["RetailPrice"] == 'Цена по запросу':
            retail_price = None
        else:
            retail_price = float(i["RetailPrice"])
        if i["Price2"] == 'Цена по запросу':
            price2 = None
        else:
            price2 = float(i["Price2"])

        if i["CustPrice"] == 'Цена по запросу':
            cust_price = None
        else:
            cust_price = float(i["CustPrice"])
        if i.get("SupOnhandDetail"):
            partner_qty = float(i["SupOnhandDetail"]["PartnerQTY"])
            partner_uom = i["SupOnhandDetail"]["PartnerUOM"]
            last_upd_date = datetime.strptime(i["SupOnhandDetail"]["LastUpdDate"], "%Y%m%d")
        else:
            partner_qty = None
            partner_uom = None
            last_upd_date = None
        try:
            from product.models import Product
            Product.objects.filter(ItemID=i["ItemId"]).update(
                AnalitCat=i["AnalitCat"],
                QTY=qty,
                SumQTY=float(sum_qty),
                Price2=price2,
                RetailPrice=retail_price,
                RetailCurrency=i["RetailCurrency"],
                CustPrice=cust_price,
                PartnerQTY=partner_qty,
                PartnerUOM=partner_uom,
                LastUpdDate=last_upd_date
            )
        except Exception as e:
            print(i)
            print(e)

    clear_directory()


def start_scheduler(*args, **kwargs):
    from apscheduler.jobstores.memory import MemoryJobStore
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.interval import IntervalTrigger

    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(MemoryJobStore(), "default")

    scheduler.add_job(
        update,
        IntervalTrigger(days=1),
        id="pricat",
        name="pricat",
        replace_existing=True,
    )
    scheduler.add_job(
        start_prodat,
        CronTrigger(day_of_week='mon', timezone=pytz.timezone(settings.TIME_ZONE)),
        id="prodat",
        name="prodat",
        replace_existing=True,
    )
    scheduler.start()
