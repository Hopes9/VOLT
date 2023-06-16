import asyncio
import mmap
import os
from threading import Thread

import xmltodict
from django.db import connections

from VOLT.settings import BASE_DIR
from product.ftp import getfile, getfile_zip
from product.models import FeatureETIMDetails_Data
from service.createAnalog import update_or_create_analog
from service.createCatalogBrashure import create_catalog_brochure
from service.createCertifi import create_certificate_info
from service.createCountry import create_country
from service.createFeature import create_feature_etim_details, feature_etim_details_data_objects
from service.createOther import create_others
from service.createProduct import update_or_create_product
from service.create_brand_series import process_product_series_brand


async def run_parallel_functions(i, main_product):
    connection = connections['default']
    main_product_id = main_product.id
    task1 = asyncio.create_task(update_or_create_analog(i, main_product_id, connection))
    task2 = asyncio.create_task(process_product_series_brand(i, main_product, connection))
    task3 = asyncio.create_task(create_country(i, main_product_id, connection))
    task4 = asyncio.create_task(create_catalog_brochure(i, main_product_id, connection))
    task5 = asyncio.create_task(create_certificate_info(i, main_product_id, connection))
    task6 = asyncio.create_task(create_feature_etim_details(i, main_product_id, connection))
    task7 = asyncio.create_task(create_others(i, main_product, connection, main_product_id))
    await asyncio.gather(task1, task2, task3, task4, task5, task6, task7)


def between_callback(i, main_product):
    asyncio.run(run_parallel_functions(i, main_product))


def start_prodat():
    xml_dict = getfile_zip("service.russvet.ru", "prodat", "bT6tsv3", "/sklad/TULA/",
                           f"{BASE_DIR}/staticfiles/prodat/")
    data = xml_dict["Document"]["DocDetail"]

    count = 0
    len_data = len(data)

    for i in data:
        count += 1
        print(f"{round(100 / (len_data / count), 3)}% {count}")
        main_product, main_product_id = update_or_create_product(i)
        thread = Thread(target=between_callback, args=(i, main_product))
        thread.start()
        if count % 1000:
            thread.join()
    FeatureETIMDetails_Data.objects.all().delete()
    FeatureETIMDetails_Data.objects.bulk_create(feature_etim_details_data_objects)
    clear_directory()


def clear_directory(directory_path=f'{BASE_DIR}/staticfiles/prodat/'):
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            clear_directory(file_path)
            os.rmdir(file_path)