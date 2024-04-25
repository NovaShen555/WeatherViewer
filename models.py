from django.db import models
    
# 用于保存一起更新的东西的更新时间
# 比如地图上的标记，还有天气数值排行那里
class UpdateTime(models.Model):
    timeid = models.CharField(max_length=50)
    deltatime = models.DateField()
    
# 地图上城市天气标记
class WeatherSignData(models.Model):
    type = models.IntegerField() # 行政级别
    url = models.CharField(max_length=5) # 后五位url
    city = models.CharField(max_length=10) # 城市名
    latitude = models.FloatField() # 纬度
    longitude = models.FloatField() # 经度
    
    # 高温 
    high_temp = models.IntegerField()
    # 早上
    m_weather_name = models.CharField(max_length=10) # 天气名
    m_weather_img = models.CharField(max_length=3) # 对应的图片编号
    m_wind_direction = models.CharField(max_length=5) # 风向
    m_wind_power = models.CharField(max_length=5) # 风力
    # 低温
    low_temp = models.IntegerField()
    # 晚上
    w_weather_name = models.CharField(max_length=10) # 天气名
    w_weather_img = models.CharField(max_length=3) # 对应的图片编号
    w_wind_direction = models.CharField(max_length=5) # 风向
    w_wind_power = models.CharField(max_length=5) # 风力
    
    belongs = models.CharField(max_length=5) # 所属的市级辖区代码 比如ANM
    postid = models.CharField(max_length=6) # 邮政编码
    
# 地图组件的首府标记
class CapitalSignData(WeatherSignData):
    pass
    
# 预警标记
class AlarmData(models.Model):
    alarmid = models.CharField(max_length=50) # 对应的编号
    headline = models.CharField(max_length=50) # 头条（不知道干啥用的）
    time = models.CharField(max_length=20) # 发生时间
    description = models.TextField() # 具体描述
    longitude = models.FloatField() # 经度
    latitude = models.FloatField() # 纬度
    img = models.CharField(max_length=20) # 图片编号
    title = models.CharField(max_length=50) # 标题
    
# 还有公告消息，气象图，城市具体天气数值没做，我中午回来搞
    