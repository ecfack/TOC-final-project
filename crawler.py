import requests
from bs4 import BeautifulSoup

def fetch_sun_time():
    r=requests.get("https://sunrise.maplogs.com/zh-TW/taiwan.777.html")

    if r.status_code == requests.codes.OK:
        soup= BeautifulSoup(r.text,'html.parser')

    sun_times=soup.find_all("span",class_="sun-time",limit=4)
    sunrise_times=list()
    for i in range(0,4):
        sunrise_times.append(sun_times[i].text)
    return sunrise_times