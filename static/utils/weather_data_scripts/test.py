from selenium import webdriver

# 启动 Chrome 浏览器
driver = webdriver.Edge()

# 打开网页
driver.get("https://weather.cma.cn/")

# 执行 JavaScript 代码，获取整个文档的源代码，包括 Shadow DOM
page_source_with_shadow_dom = driver.execute_script("return document.documentElement.outerHTML")

# 关闭浏览器
driver.quit()

# 打印网页源代码
with open('testmain.html','w',encoding='utf-8') as f:
    f.write(page_source_with_shadow_dom)