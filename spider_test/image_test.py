import requests
from selenium import webdriver
from lxml import etree
from selenium import webdriver
from matplotlib import pyplot as plt
from PIL import Image
import time

# headers = {
#     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
#     'Accept-Encoding':'gzip, deflate',
#     'Accept-Language':'zh-CN,zh;q=0.9',
#     'Cache-Control':'max-age=0',
#     'Upgrade-Insecure-Requests':'1',
#     'Host':'www.mayidaili.com',
#     'Proxy-Connection': 'keep-alive',
#     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
# }
# Cookies = {
#     'Hm_lvt_dad083bfc015b67e98395a37701615ca':'',
#     'Hm_lpvt_dad083bfc015b67e98395a37701615ca':'',
#     'proxy_token':'',
# }
#
# options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# options.add_argument("--disable-gpu")
# driver = webdriver.Chrome(options=options)
# response = driver.get('http://www.mayidaili.com/free')
# cookies = driver.get_cookies()
# Cookies['proxy_token'] = cookies[1]['value']
# Cookies['Hm_lvt_dad083bfc015b67e98395a37701615ca'] = cookies[0]['value']
# Cookies['Hm_lpvt_dad083bfc015b67e98395a37701615ca'] = cookies[2]['value']
# print(Cookies)
# port_url = 'http://www.mayidaili.com/free/img/1/17574/VdzjQL1S_UyJ4ZSYXQYj3Q'
# images = requests.get(port_url,headers=headers,cookies=Cookies)
# with open('y.jpg','wb') as f:
#     f.write(images.content)

import PIL
import requests
import numpy as np
import pytesseract


from lxml import etree
from selenium import webdriver
from matplotlib import pyplot as plt

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)

url = "http://www.mayidaili.com/free/1"

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
 'Accept-Encoding': 'gzip, deflate',
 'Accept-Language': 'zh-CN,zh;q=0.9',
 'Cache-Control': 'max-age=0',
 'Connection': 'keep-alive',
 'Cookie': 'Hm_lvt_dad083bfc015b67e98395a37701615ca=1554796082; JSESSIONID=C6FF5039054C48DCFDB16B97F1174DA5; proxy_token=xACHriPa; Hm_lpvt_dad083bfc015b67e98395a37701615ca=1554808505',
 'Host': 'www.mayidaili.com',
 'Upgrade-Insecure-Requests': '1',
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

if __name__ == "__main__":
    url = "http://www.mayidaili.com/free/{i}"
    session = requests.Session()
    for i in range(1, 5928):
        url_ = url.format(i=i)
        print(url_.center(100, "*"))
        response = driver.get(url_)
        content = driver.page_source
        html = etree.HTML(content)
        ips       = list(map(lambda obj: obj.strip(), html.xpath("//tr/td[1]/text()")))
        port_imgs = html.xpath("//tr/td[2]/img[@class='js-proxy-img']/@src")
		# 这个是遇到的一个坑，使用浏览器产生的headers时，status_code是成功的
		# 但是图片是下载不到的，最后用这种方式搞定。
        cookies = driver.get_cookies()
        s = ""
        for cookie in cookies:
            s += "{}={}; ".format(cookie['name'], cookie['value'])
        s = s[:-2]
        headers["Cookie"] = s
        ports = []
        for img in port_imgs:
            images = requests.get(img, headers=headers)
            if images.status_code == 200:
                with open("test.jpg", 'wb') as file:
                    for chunk in images.iter_content(128):
                        file.write(chunk)
            img = PIL.Image.open('test.jpg')
            img = np.array(img)
            img_ = np.array(list(map(lambda obj: obj if obj < 1 else 255, img.ravel()))).reshape(img.shape)
            img = PIL.Image.fromarray(img_.astype(np.uint8))
            port = pytesseract.image_to_string(img,config='-psm 8 outputbase digits')
            port_l = list(port)
            for i in range(0,len(port_l)):
                if port_l[i] == '5':
                    port_l[i] = '8'
            x = ''.join(port_l)
            if x == '2128':
                ports.append('3128')
            elif x == '2129':
                ports.append('3129')
            else:
                ports.append(x)
        for ip,port in zip(ips,ports):
            address = ip + ':' + port
            print(address)

