import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from WeatherViewer.models import CityInfo,UpdateTime
import time
import json

def update_city_weather():
    try:
        obj = UpdateTime.objects.get(
            timeid = 'updatecity'
        )
    except CityInfo.DoesNotExist:
        obj = UpdateTime(
            timeid = 'updatecity',
            deltatime = timezone.now().date() + timezone.timedelta(days=-1)
        )
    except UpdateTime.MultipleObjectsReturned:
        all_obj = CityInfo.objects.filter(
            timeid = 'updatecity'
        )
        all_obj.delete()
        obj = UpdateTime(
            timeid = 'updatecity',
            deltatime = timezone.now().date() + timezone.timedelta(days=-1)
        )
    
    head = "https://weather.cma.cn/api/map/weather/1?t="
    url = head + str(int(time.time() * 1000))
    response = requests.get(url)
    while response.status_code != 200:
        response = requests.get(url)
    text_data = json.load(response.text)
    
