from bs4 import BeautifulSoup
import urllib.request

url = 'https://weather.cma.cn/assets/cma/img/weather_bg.jpg'
urllib.request.urlretrieve(url,'urlweather_bg.jpg')