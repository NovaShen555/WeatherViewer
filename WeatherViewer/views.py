from django.shortcuts import render, redirect
import json
from django.http import HttpResponse
import requests
import time
from bs4 import BeautifulSoup
from lxml import html
from datetime import datetime
from static.utils.data.province_border import province_border
from static.utils.data.province_data import province_data


def jumptohome(request):
    return redirect('home')

def home(request):
    url = "https://weather.cma.cn/api/map/weather/1"
    response = requests.get(url)
    city_data = response.text
    return render(request, 'home.html', {
        'province_border': province_border,
        'province_data': province_data,
        'city_data_json': city_data
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
    head = "https://weather.cma.cn/api/map/weather/1?t="
    url = head + str(int(time.time() * 1000))
    response = requests.get(url)
    city_data = response.text
    """
    # 将中心点坐标添加到 GeoJSON 数据中的属性中
    for feature in china_province['features']:
        province_name = feature['properties']['name']
        if province_name in capital_data:
            # 使用列表解析将字符串转换为浮点数列表
            coordinates = [float(coord) for coord in capital_data[province_name]]
            feature['properties']['centroid'] = coordinates
    """
    return render(request, 'weathermap.html', {
        'city_data_json': city_data
    })


def weather_report(request):
    head = "https://weather.cma.cn/api/map/weather/1?t="
    url = head + str(int(time.time() * 1000))
    response = requests.get(url)
    city_data = response.text
    return render(request, 'toolmap.html', {
        'city_data_json': city_data
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
        today = datetime.today()
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
    # url = "https://weather.cma.cn/web/weather/53463.html"
    # response = requests.get(url)
    # response.encoding = 'utf-8'
    # soup = BeautifulSoup(response.text, 'html.parser')
    # view_weather = soup.find_all("div", class_="col-xs-12")
    # view_weather = view_weather[0]
    # with open("templates/view_weather.html", "w", encoding='utf-8') as f:
    #     f.write(view_weather.prettify())
    # print(view_weather.prettify())
    #
    # url = 'https://weather.cma.cn/web/weather/' + str(city_index)
    # response = requests.get(url)
    # with open("templates/city_weather_from_web.html", "w", encoding='utf-8') as f:
    #     # f.write(response.text)
    #     soup = BeautifulSoup(response.text, "html.parser")
    #     items = soup.find_all("div", class_="col-xs-9")
    #     items = items[0]
    #     f.write(items.prettify())
    # print(city_index)
    # head = "https://weather.cma.cn/web/weather/"
    # url = head + str(city_index)
    # response = requests.get(url)
    # if response.status_code != 200:
    #     return jumptohome(request)
    return render(request, "city_weather.html")


def test(request):
    return render(request, "test.html")