from django.shortcuts import render, redirect
import json
from django.http import HttpResponse
import requests
import time
from bs4 import BeautifulSoup
from lxml import html,etree
from datetime import datetime

from WeatherViewer.models import bulletinData
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
    resp = requests.get(url)

    resp.encoding = 'utf-8'
    tree = html.fromstring(resp.content)
    # 应用XPath表达式，选择需要的元素

    bulletin_home = tree.xpath('/html/body/nav[3]/div/a[3]')[0]
    bulletin_home_url = "https://weather.cma.cn" + bulletin_home.attrib['href']

    resp = requests.get(bulletin_home_url)
    resp.encoding = 'utf-8'
    tree = html.fromstring(resp.content)

    a_data = tree.xpath('/html/body/div[1]/div[2]/div[1]/div/div[2]//a')
    hrefs = ["https://weather.cma.cn" + a.get('href') for a in a_data]
    print(hrefs)
    bulletinData.objects.all().delete()
    tid = 0
    for b_url in hrefs:
        tid += 1
        print(b_url)
        resp = requests.get(b_url)
        resp.encoding = 'utf-8'
        tree = html.fromstring(resp.content)
        content = tree.xpath('/html/body/div[1]/div[2]/div[2]')
        # print(html.tostring(content[0], pretty_print=True).decode())
        new_bulletin = bulletinData(tid=tid, content=html.tostring(content[0], pretty_print=True).decode())
        new_bulletin.save()



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
        print(new_str)
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

    url = 'https://weather.cma.cn/web/weather/' + str(city_index)
    response = requests.get(url)
    response.encoding = 'utf-8'
    html_content = response.content
    tree = html.fromstring(html_content)
    # 应用XPath表达式，选择需要的元素
    head_data = tree.xpath('/html/body/div[1]/div')
    print(html.tostring(head_data[0], pretty_print=True).decode())
    with open("templates/view_weather.html", "w", encoding='utf-8') as f:
        f.write(html.tostring(head_data[0], pretty_print=True).decode())

    with open("templates/city_weather_from_web.html", "w", encoding='utf-8') as f:
        f.write(html.tostring(head_data[1], pretty_print=True).decode())

    qwe = requests.get(url)
    if qwe.status_code != 200:
        return jumptohome(request)
    return render(request, "city_weather.html")


def test(request):
    return render(request, "test.html")