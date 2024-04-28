from django.db.models import Max
from django.shortcuts import render, redirect
import json
from django.http import HttpResponse, HttpResponsePermanentRedirect
import requests
import time
from bs4 import BeautifulSoup
from lxml import html, etree
from datetime import datetime

from WeatherViewer.models import bulletinData, CityInfo, weatherData
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

    city = CityInfo.objects.filter(cityname__contains=query)
    if city:
        print(city[0].cityname)
        return HttpResponsePermanentRedirect(city[0].cityurl)

    return HttpResponsePermanentRedirect("/home")


def weather_map(request):
    head = "https://weather.cma.cn/api/map/weather/1?t="
    url = head + str(int(time.time() * 1000))
    response = requests.get(url)
    city_data = response.text
    return render(request, 'weathermap.html', {
        'city_data_json': city_data
    })


def weather_report(request):
    url = "https://weather.cma.cn/api/map/weather/1"
    response = requests.get(url)
    city_data = response.text
    return render(request, 'toolmap.html', {
        'city_data_json': city_data,
        'province_border': province_border,
        'province_data': province_data
    })


def graphs(request):
    return render(request, 'weather_graphs.html')


# Meteorological bulletins
def bulletins(request, msg_index=None):
    # url = 'https://weather.cma.cn'
    # resp = requests.get(url)
    #
    # resp.encoding = 'utf-8'
    # tree = html.fromstring(resp.content)
    # # 应用XPath表达式，选择需要的元素
    #
    # bulletin_home = tree.xpath('/html/body/nav[3]/div/a[3]')[0]
    # bulletin_home_url = "https://weather.cma.cn" + bulletin_home.attrib['href']
    #
    # resp = requests.get(bulletin_home_url)
    # resp.encoding = 'utf-8'
    # tree = html.fromstring(resp.content)
    #
    # a_data = tree.xpath('/html/body/div[1]/div[2]/div[1]/div/div[2]//a')
    # hrefs = ["https://weather.cma.cn" + a.get('href') for a in a_data]
    # print(hrefs)
    # bulletinData.objects.all().delete()
    # tid = 0
    # for b_url in hrefs:
    #     tid += 1
    #     print(b_url)
    #     resp = requests.get(b_url)
    #     resp.encoding = 'utf-8'
    #     tree = html.fromstring(resp.content)
    #     content = tree.xpath('/html/body/div[1]/div[2]/div[2]')
    #     title = tree.xpath('normalize-space(/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div//text())')
    #     print(title)
    #     new_bulletin = bulletinData(tid=tid,title=title, content=html.tostring(content[0], pretty_print=True).decode())
    #     new_bulletin.save()

    if msg_index is None:
        msg_index = 1

    max_tid = bulletinData.objects.aggregate(max_tid=Max('tid'))['max_tid']
    if int(msg_index) > max_tid:
        return jumptohome(request)

    bulletin = bulletinData.objects.get(tid=msg_index)
    titles = [(str(i), bulletinData.objects.get(tid=i).title) for i in range(1, max_tid + 1)]

    data = {'bulletin': bulletin, 'titles': titles, 'msg_index': msg_index}

    return render(request, "bulletins_base.html", data)


def alarm_map(request):
    url = "https://weather.cma.cn/api/map/alarm"
    response = requests.get(url)
    city_data = response.text
    return render(request, 'alarmmap.html', {
        'city_data_json': city_data
    })


def get_city_weather(request, city_index):
    print(city_index)

    # url = 'https://weather.cma.cn/web/weather/' + str(city_index)
    # response = requests.get(url)
    # response.encoding = 'utf-8'
    # html_content = response.content
    # tree = html.fromstring(html_content)
    # # 应用XPath表达式，选择需要的元素
    # head_data = tree.xpath('/html/body/div[1]/div')
    # print(html.tostring(head_data[0], pretty_print=True).decode())
    # with open("templates/view_weather.html", "w", encoding='utf-8') as f:
    #     f.write(html.tostring(head_data[0], pretty_print=True).decode())
    #
    # with open("templates/city_weather_from_web.html", "w", encoding='utf-8') as f:
    #     f.write(html.tostring(head_data[1], pretty_print=True).decode())
    #
    # qwe = requests.get(url)
    # if qwe.status_code != 200:
    #     return jumptohome(request)


    weather = weatherData.objects.filter(city_id=city_index)
    if weather:
        weather = weather[0]
        update_date = weather.update_date
        upper = weather.upper_content
        lower = weather.lower_content
        return render(request, "city_weather.html", {
            'upper': upper,
            'lower': lower,
            'update_date': update_date
        })

    return HttpResponsePermanentRedirect("/home")

def redirect_to_file(request):
    original_uri = request.get_full_path()
    print(original_uri)
    new_uri = "https://weather.cma.cn" + original_uri
    return HttpResponsePermanentRedirect(new_uri)

def test(request):
    url = "https://weather.cma.cn/api/map/weather/1"
    response = requests.get(url)
    data = response.json()
    cities = [
        {'id':sublist[0],'url': "../weather/" + sublist[0], 'name': sublist[1],'WeatherUpdateDate':data["data"]["date"].replace("/","-")}
        for sublist in data['data']['city']
    ]

    for city in cities:
        time.sleep(1)
        print(city)
        url = 'https://weather.cma.cn/web/weather/' + city['url'].split("/")[-1]
        print(url)
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        html_content = resp.content
        tree = html.fromstring(html_content)
        # 应用XPath表达式，选择需要的元素
        head_data = tree.xpath('/html/body/div[1]/div')

        upper = html.tostring(head_data[0], pretty_print=True).decode()
        lower = html.tostring(head_data[1], pretty_print=True).decode()

        city_weather = weatherData(city_id=city['id'], upper_content=upper, lower_content=lower, update_date=city['WeatherUpdateDate'])
        city_weather.save()

    return HttpResponse("1")
