import secrets
import string

from product.models import RsCatalog


def find_by_key(iterable, key, value):
    for index, dict_ in enumerate(iterable):
        if key in dict_ and dict_[key] == value:
            return dict_


def find_all_by_key(iterable, key, value):
    dicts = []
    for index, dict_ in enumerate(iterable):
        if key in dict_ and dict_[key] == value:
            dicts.append(dict_)
    return dicts


def dict_fetch_all(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_secret_key_():
    rand_string = "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16))
    return rand_string


def update_catalog():
    catalog = []
    rows_level4 = RsCatalog.objects.all().distinct("Level4ID")
    for row in rows_level4:
        catalog.append({"Level4ID": row.Level4ID, "Level4Name": row.Level4Name})

    for h in catalog:
        h["Level3"] = list(
            RsCatalog.objects.filter(Level4ID=h["Level4ID"]).distinct("Level3ID").values("Level3ID", "Level3Name"))
    for g in catalog:
        for i in g["Level3"]:
            i["Level2"] = list(
                RsCatalog.objects.filter(Level3ID=i["Level3ID"]).distinct("Level2ID").values("Level2ID", "Level2Name"))
    return catalog


def chek_list_int(l):
    try:
        return list(map(int, l.split(",")))
    except:
        return []


def percent(part, whole):
    try:
        return 100 * float(part) / float(whole)
    except ZeroDivisionError:
        return 0
