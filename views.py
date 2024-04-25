from django.shortcuts import render, redirect
import json
from django.http import HttpResponse
import requests
import time
from bs4 import BeautifulSoup
from lxml import html
from static.utils.data.province_border import province_border
from static.utils.data.province_data import province_data
from .models import UpdateTime,WeatherSignData,AlarmData,CapitalSignData
from django.utils import timezone
from django.core.serializers import serialize
import datetime
from django.db import transaction


def jumptohome(request):
    return redirect('home')

def home(request):
    # 检验一下会不会报错
    try:
        timekeeper = UpdateTime.objects.get(
            timeid = "WeatherSignData"
        )
    except UpdateTime.DoesNotExist:
        timekeeper = UpdateTime(
            timeid = "WeatherSignData",
            deltatime = timezone.now().date() + timezone.timedelta(days=-1)
        )
        timekeeper.save()
    except UpdateTime.MultipleObjectsReturned:
        all_obj = UpdateTime.objects.filter(
            timeid = "WeatherSignData"
        )
        all_obj.delete()
        
        timekeeper = UpdateTime(
            timeid = "WeatherSignData",
            deltatime = timezone.now().date() + timezone.timedelta(days=-1)
        )
        timekeeper.save()
        
    timekeeper = UpdateTime.objects.get(
        timeid = "WeatherSignData"
    )
    if timekeeper.deltatime < timezone.now().date():
        url = "https://weather.cma.cn/api/map/weather/1"
        response = requests.get(url)
        city_data = response.text
        
        city_data = json.loads(response.text)
    #if True:
        with transaction.atomic():
            for city in city_data['data']['city']:
                try:
                    obj = WeatherSignData.objects.get(
                        url = city[0]
                    )
                    obj.delete()
                except WeatherSignData.DoesNotExist:
                    pass
                except WeatherSignData.MultipleObjectsReturned:
                    all_obj = WeatherSignData.objects.filter(
                        url = city[0]   
                    )
                    all_obj.delete()
                finally:
                    obj = WeatherSignData(
                        url = city[0], # 后五位url
                        city = city[1], # 城市名
                        type = city[3], # 行政级别
                        latitude = city[4], # 纬度
                        longitude = city[5], # 经度
                        # 高温 
                        high_temp = city[6],
                        # 早上
                        m_weather_name = city[7], # 天气名
                        m_weather_img = city[8], # 对应的图片编号
                        m_wind_direction = city[9], # 风向
                        m_wind_power = city[10], # 风力
                        # 低温
                        low_temp = city[11],
                        # 晚上
                        w_weather_name = city[12], # 天气名
                        w_weather_img = city[13], # 对应的图片编号
                        w_wind_direction = city[14], # 风向
                        w_wind_power = city[15], # 风力
                        
                        belongs = city[16], # 所属的市级辖区代码 比如ANM
                        postid = city[17] # 邮政编码
                    )
                    obj.save()
                
        timekeeper.deltatime = timezone.now().date()
        timekeeper.save()
        
    city_data_json = serialize('json', WeatherSignData.objects.all())
    
    with open("datasets/province_bound.geojson","r",encoding="utf-8") as f:
        china_province = json.load(f)
        
    with open("datasets/maincity.json","r",encoding="utf-8") as f:
        capital_data_json = json.load(f)
    
    return render(request, 'home.html', {
        'city_data_json': city_data_json,
        'capital_data_json':json.dumps(capital_data_json),
        'china_province':json.dumps(china_province),
        'DateTime': timezone.now().date().strftime('%Y/%m/%d')
    })


def search_results(request):
    query = request.GET.get('query')

    head = "https://weather.cma.cn/api/map/weather/1?t="
    url = head + str(int(time.time() * 1000))
    response = requests.get(url)
    data = response.json()
    cities = [
        {'url': "../wheather/" + sublist[0], 'name': sublist[1]}
        for sublist in data['data']['city']
        if len(sublist) >= 2 and sublist[1] == query
    ]
    for city in cities:
        print(city)
    # Perform search logic here
    # Return search results page
    return render(request, 'search.html', {
        'query': query,
        'cities': json.dumps(cities)
    })


def search_ex(request):
    return render(request, 'test_data3.html')


def weather_map(request):
    # 检验一下会不会报错
    try:
        timekeeper = UpdateTime.objects.get(
            timeid = "WeatherSignData"
        )
    except UpdateTime.DoesNotExist:
        timekeeper = UpdateTime(
            timeid = "WeatherSignData",
            deltatime = timezone.now().date() + timezone.timedelta(days=-1)
        )
        timekeeper.save()
    except UpdateTime.MultipleObjectsReturned:
        all_obj = UpdateTime.objects.filter(
            timeid = "WeatherSignData"
        )
        all_obj.delete()
        
        timekeeper = UpdateTime(
            timeid = "WeatherSignData",
            deltatime = timezone.now().date() + timezone.timedelta(days=-1)
        )
        timekeeper.save()
        
    timekeeper = UpdateTime.objects.get(
        timeid = "WeatherSignData"
    )
    if timekeeper.deltatime < timezone.now().date():
        url = "https://weather.cma.cn/api/map/weather/1"
        response = requests.get(url)
        response.encoding = 'uft-8'
        
        city_data = json.loads(response.text)
    #if True:
        with transaction.atomic():
            for city in city_data['data']['city']:
                try:
                    obj = WeatherSignData.objects.get(
                        url = city[0]
                    )
                    obj.delete()
                except WeatherSignData.DoesNotExist:
                    pass
                except WeatherSignData.MultipleObjectsReturned:
                    all_obj = WeatherSignData.objects.filter(
                        url = city[0]   
                    )
                    all_obj.delete()
                finally:
                    obj = WeatherSignData(
                        url = city[0], # 后五位url
                        city = city[1], # 城市名
                        type = city[3], # 行政级别
                        latitude = city[4], # 纬度
                        longitude = city[5], # 经度
                        # 高温 
                        high_temp = city[6],
                        # 早上
                        m_weather_name = city[7], # 天气名
                        m_weather_img = city[8], # 对应的图片编号
                        m_wind_direction = city[9], # 风向
                        m_wind_power = city[10], # 风力
                        # 低温
                        low_temp = city[11],
                        # 晚上
                        w_weather_name = city[12], # 天气名
                        w_weather_img = city[13], # 对应的图片编号
                        w_wind_direction = city[14], # 风向
                        w_wind_power = city[15], # 风力
                        
                        belongs = city[16], # 所属的市级辖区代码 比如ANM
                        postid = city[17] # 邮政编码
                    )
                    obj.save()
                
        timekeeper.deltatime = timezone.now().date()
        timekeeper.save()
        
    city_data_json = serialize('json', WeatherSignData.objects.all())
    
    
    with open("datasets/province_bound.geojson","r",encoding="utf-8") as f:
        china_province = json.load(f)
        
    with open("datasets/maincity.json","r",encoding="utf-8") as f:
        capital_data_json = json.load(f)
    
    return render(request, 'weathermap.html', {
        'city_data_json': city_data_json,
        'capital_data_json':json.dumps(capital_data_json),
        'china_province':json.dumps(china_province),
        'DateTime': timezone.now().date().strftime('%Y/%m/%d')
    })


def weather_report(request):
    # 检验一下会不会报错
    try:
        timekeeper = UpdateTime.objects.get(
            timeid = "WeatherSignData"
        )
    except UpdateTime.DoesNotExist:
        timekeeper = UpdateTime(
            timeid = "WeatherSignData",
            deltatime = timezone.now().date() + timezone.timedelta(days=-1)
        )
        timekeeper.save()
    except UpdateTime.MultipleObjectsReturned:
        all_obj = UpdateTime.objects.filter(
            timeid = "WeatherSignData"
        )
        all_obj.delete()
        
        timekeeper = UpdateTime(
            timeid = "WeatherSignData",
            deltatime = timezone.now().date() + timezone.timedelta(days=-1)
        )
        timekeeper.save()
        
    timekeeper = UpdateTime.objects.get(
        timeid = "WeatherSignData"
    )
    if timekeeper.deltatime < timezone.now().date():
        url = "https://weather.cma.cn/api/map/weather/1"
        response = requests.get(url)
        city_data = response.text
        
        city_data = json.loads(response.text)
    #if True:
        with transaction.atomic():
            for city in city_data['data']['city']:
                try:
                    obj = WeatherSignData.objects.get(
                        url = city[0]
                    )
                    obj.delete()
                except WeatherSignData.DoesNotExist:
                    pass
                except WeatherSignData.MultipleObjectsReturned:
                    all_obj = WeatherSignData.objects.filter(
                        url = city[0]   
                    )
                    all_obj.delete()
                finally:
                    obj = WeatherSignData(
                        url = city[0], # 后五位url
                        city = city[1], # 城市名
                        type = city[3], # 行政级别
                        latitude = city[4], # 纬度
                        longitude = city[5], # 经度
                        # 高温 
                        high_temp = city[6],
                        # 早上
                        m_weather_name = city[7], # 天气名
                        m_weather_img = city[8], # 对应的图片编号
                        m_wind_direction = city[9], # 风向
                        m_wind_power = city[10], # 风力
                        # 低温
                        low_temp = city[11],
                        # 晚上
                        w_weather_name = city[12], # 天气名
                        w_weather_img = city[13], # 对应的图片编号
                        w_wind_direction = city[14], # 风向
                        w_wind_power = city[15], # 风力
                        
                        belongs = city[16], # 所属的市级辖区代码 比如ANM
                        postid = city[17] # 邮政编码
                    )
                    obj.save()
                
        timekeeper.deltatime = timezone.now().date()
        timekeeper.save()
        
    city_data_json = serialize('json', WeatherSignData.objects.all())
    
    
    with open("datasets/province_bound.geojson","r",encoding="utf-8") as f:
        china_province = json.load(f)
        
    with open("datasets/maincity.json","r",encoding="utf-8") as f:
        capital_data_json = json.load(f)
    
    return render(request, 'toolmap.html', {
        'city_data_json': city_data_json,
        'capital_data_json':json.dumps(capital_data_json),
        'china_province':json.dumps(china_province),
        'DateTime': timezone.now().date().strftime('%Y/%m/%d')
    })


def graphs(request):
    return render(request, 'weather_graphs.html')


# Meteorological bulletins
def bulletins(request, msg_index=None):
    if msg_index is None:
        msg_index = 1
    url = 'https://weather.cma.cn'
    response = requests.get(url)
    html_content = response.content
    tree = html.fromstring(html_content)
    # 应用XPath表达式，选择需要的链接元素
    # 获取链接元素的href属性，即链接的URL
    bulletins_url = tree.xpath('/html/body/nav[3]/div/a[3]')[0].get('href')

    response = requests.get(url + '/web' + bulletins_url)
    html_content = response.content
    tree = html.fromstring(html_content)

    head = "/html/body/div[1]/div[2]/div[1]/div/div[2]/a["
    tail = "]"
    urls = []
    for i in range(1, 9):
        urls.append(tree.xpath(head + str(i) + tail)[0].attrib['href'])
    new_str = tree.xpath(head + str(msg_index) + tail)[0].attrib['href']
    # urls.append(new_str)
    with open("templates/bulletin.html", "w", encoding='utf-8') as f:
        print(type(new_str))
        response = requests.get(url + new_str)
        response.encoding = 'utf-8'
        content_str = response.text
        # 获取当前日期
        today = timezone.now().date()
        # 格式化日期为 '年/月/日' 格式
        formatted_date = today.strftime('/file/%Y/%m/%d')
        content_str = content_str.replace(formatted_date, "https://weather.cma.cn" + formatted_date)
        for i in range(1, 9):
            content_str = content_str.replace(urls[i - 1], str(i))
        soup = BeautifulSoup(content_str, "html.parser")
        datas = soup.find_all("div", class_="container")
        data = datas[3].find_all("div", class_="hp mt15")
        data[0].extract()
        f.write(datas[3].prettify())

    return render(request, "bulletins_base.html")


def alarm_map(request):
    url = "https://weather.cma.cn/api/map/alarm"
    response = requests.get(url)
    city_data = response.text
    return render(request, 'alarmmap.html', {
        'city_data_json': city_data
    })


def get_city_weather(request, city_index):
    print(city_index)
    url = "https://weather.cma.cn/web/weather/53463.html"
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    view_weather = soup.find_all("div", class_="col-xs-12")
    view_weather = view_weather[0]
    with open("templates/view_weather.html", "w", encoding='utf-8') as f:
        f.write(view_weather.prettify())
    print(view_weather.prettify())

    url = 'https://weather.cma.cn/web/weather/' + str(city_index)
    response = requests.get(url)
    with open("templates/city_weather_from_web.html", "w", encoding='utf-8') as f:
        # f.write(response.text)
        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find_all("div", class_="col-xs-9")
        items = items[0]
        f.write(items.prettify())
    print(city_index)
    head = "https://weather.cma.cn/web/weather/"
    url = head + str(city_index)
    response = requests.get(url)
    if response.status_code != 200:
        return jumptohome(request)
    return render(request, "city_weather.html")
