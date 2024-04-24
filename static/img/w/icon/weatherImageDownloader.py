import urllib.request

head = "https://weather.cma.cn/static/img/w/icon/w"
tail = ".png"
filehead = "static/images/w"

for i in range(0,36):
    url = head + str(i) + tail
    file_path = filehead + str(i) +tail
    try:
        urllib.request.urlretrieve(url, file_path)
        print("文件下载成功！")
    except Exception as e:
        print("下载失败:", e)

