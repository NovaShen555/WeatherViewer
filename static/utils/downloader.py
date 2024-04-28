import requests
import os

def download_files(links, base_url):
    for link in links:
        try:
            # 构建完整的下载链接
            download_url = base_url + link
            # 去掉前缀部分作为文件路径
            filename = link.lstrip('/')
            # 分割路径和文件名
            dir_name, file_name = os.path.split(filename)
            # 创建目录（如果不存在）
            os.makedirs(dir_name, exist_ok=True)
            # 下载文件
            response = requests.get(download_url)
            if response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded {filename} successfully.")
            else:
                print(f"Failed to download {filename}: {response.status_code}")
        except Exception as e:
            print(f"Failed to download {filename}: {str(e)}")

# 提供的链接列表
links = [
    "/static/SuperSlide/jquery.SuperSlide.2.1.js"
]

# 基础 URL 前缀
base_url = "https://weather.cma.cn"

# 下载文件
download_files(links, base_url)