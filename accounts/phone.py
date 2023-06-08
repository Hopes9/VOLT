import requests
from greensms.client import GreenSMS

key_net_tel = "4cb31ac9ea15133411fe586417f9038ec92b830cb34cc864"
write_key = "849005002b4cedbb79504189c5600dede2da21bf1b4500db"


def call_phone(number):
    client = GreenSMS(user='tmSHE', password='1z8@9F$Rn7b9',
                      token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidG1TSEUiLCJpYXQiOjE2NzUyNTkxOTIsImlzcyI6ImFwaS5ncmVlbnNtcy5ydSJ9.sHa7OxZQC3zSgqTrEuTvXja_WHue5xD91RSM9QGoNUw')
    response = client.call.send(to=str(number))
    return response.code


def call_repeat(uid):
    url = f"https://api.ucaller.ru/v191.0/initRepeat?uid={uid}"
    response = requests.request("GET", url)
    return response.text
