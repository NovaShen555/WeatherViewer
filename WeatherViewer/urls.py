from django.urls import path
from . import views

urlpatterns = [
    path('', views.jumptohome, name='jumptohome'),
    path('home/', views.home, name='home'),
    path('search/', views.search_results, name='search_results'),
    path('guidance/',views.search_ex,name='examples'),
    path('api/weathermap',views.weather_map,name='wmap'),
    path('map/',views.weather_report,name='performap'),
    path('bulletins/<msg_index>',views.bulletins,name='bulletins'),
    path('bulletins/', views.bulletins, name='jumptobulletins'),
    path('graphs/',views.graphs,name='graphs'),
    path('alarm/',views.alarm_map,name='alarm'),
    path('weather/<city_index>',views.get_city_weather,name='get_city_weather'),
    path('test/',views.test,name='test')
]
