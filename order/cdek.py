import requests
import json

url = "https://api.cdek.ru/v2/calculator/tariff"
def get_price(address, weight):
    payload = json.dumps({
      "tariff_code": 136,
      "currency": 1,
      "to_location": {
        "address": "Кириши"
      },
      "from_location": {
        "address": "Белгород"
      },
      "weight": 500,
      "packages": [
        {
          "height": 20,
          "length": 20,
          "weight": 50,
          "width": 100
        }
      ],
      "type": 1
    })
    headers = {
      'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY29wZSI6WyJvcmRlcjphbGwiLCJwYXltZW50OmFsbCJdLCJleHAiOjE2NzU2MjU5NDUsImF1dGhvcml0aWVzIjpbImFjY291bnQtdXVpZDplZTBiM2VlMC01ZDgwLTQ1OTUtOWZkNC1hN2I3ODM0NTNiOGMiLCJjb250cmFjdDrQmNCcLdCg0KQtQkxENi0xMzQiLCJhY2NvdW50LWxhbmc6cnVzIiwic2hhcmQtaWQ6cnUtMDQiLCJjbGllbnQtZW1haWxzOmluZm9AdG1zaGUucnUiLCJhcGktdmVyc2lvbjoxLjEiLCJjbGllbnQtY2l0eTrQkdC10LvQs9C-0YDQvtC0LCDQkdC10LvQs9C-0YDQvtC00YHQutCw0Y8g0L7QsdC70LDRgdGC0YwiLCJjbGllbnQtaWQtZWM1OjM1OGYzY2MyLWMyMWUtNGY0ZS1hNTI5LWZkYTZjODFhZDhiMSIsImZ1bGwtbmFtZTrQp9Cj0JHQkNCg0J4g0JjQm9Cs0K8g0JLQm9CQ0JTQmNCc0JjQoNCe0JLQmNCnLCDQmNC90LTQuNCy0LjQtNGD0LDQu9GM0L3Ri9C5INC_0YDQtdC00L_RgNC40L3QuNC80LDRgtC10LvRjCIsImNvbnRyYWdlbnQtdXVpZDozNThmM2NjMi1jMjFlLTRmNGUtYTUyOS1mZGE2YzgxYWQ4YjEiLCJzb2xpZC1hZGRyZXNzOmZhbHNlIiwiY2xpZW50LWlkLWVjNDpudWxsIl0sImp0aSI6ImI0YzJhNTc0LTAxNDUtNDYyNi04ZTE4LWE2ZGVkMmIzOThkOCIsImNsaWVudF9pZCI6IndnUlBTaGdSWnE1dlYzTW9Fb2liVUhIWFRFNGNXdE5tIn0.Dl_ahm2bzXaG7vsjfOnQY4NQMBHJ3h-h1xDqIWOccWugPqYBDbvHebElRFllo-0QpFAtZdN7XQ4JmV-S6KajiJnLvwcAKOj-Ym7x1E2UO4MuPFBLX58rodUQ18PQU4kxW_xpxL6zv_uzytWZ22q243g6u82j1kMTj73UmaN6eFbyLgfdVksrpRshJ_5rvDsdEZeQlt9zRRk9Pp6W62mCRSM-yzStFF567cnegJ87LG4i9j6uB1frh_0YRrH6uqBgRH2lERSLtwU76ZJ71VieqkBf8cT7YPiJn4Fa3MFNpCRWBY5ZsvBkFJnO36ts9rLHH-8kb-mI8byEqfKv1YpBbQ',
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    dict(response.text).get("total_sum", None)
