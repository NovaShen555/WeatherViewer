import requests
from bs4 import BeautifulSoup
import json

def update_city_weather(urltail):
    url = 'https://weather.cma.cn/web/weather/' + str(urltail)
    response = requests.get(url)
    with open("../templates/city_weather_from_web.html","w",encoding='utf-8') as f:
        #f.write(response.text)
        soup = BeautifulSoup(response.text,"html.parser")
        items = soup.find_all("div",class_="col-xs-9")
        items = items[0]
        f.write(items.prettify())