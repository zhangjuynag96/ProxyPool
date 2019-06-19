import requests
import re
from pyquery import PyQuery as pq
from Get_Module.utils import get_page
import tesserocr
from PIL import Image
import pytesseract
import time


# mimvp

#     response = get_page('https://proxy.mimvp.com/freeopen.php?proxy=in_hp&sort=&page=1')
#     pattern = re.compile("<td class='tbl-proxy-ip' style='text-align: left;'>(\d+.\d+.\d+.\d+)</td><td class='tbl-proxy-port'><img src=(.*?) /></td><td class='tbl-proxy-type'")
#     result = pattern.findall(response)
#     for i in result:
#         url = 'https://proxy.mimvp.com/' + i[1]
#         images = requests.get(url)
#         with open('x.jpg','wb') as f:
#             f.write(images.content)
#         #灰度处理
#         image = Image.open('x.jpg')
#         image = image.convert('L')
#         threshold = 80
#         table = []
#         for j in range(256):
#             if j < threshold:
#                 table.append(0)
#             else:
#                 table.append(1)
#         image = image.point(table, '1')
#         port = pytesseract.image_to_string(image,config='-psm 7 outputbase digits')
#         if port == '3333':
#             port = '9999'

#xici
# for page in range(1,3500):
#     response = get_page('https://www.xicidaili.com/nn/{page}'.format(page=page))
#     find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
#     trs = find_trs.findall(response)
#     for tr in trs:
#         find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
#         re_ip_address = find_ip.findall(tr)
#         find_port = re.compile('<td>(\d+)</td>')
#         re_port = find_port.findall(tr)
#         for address, port in zip(re_ip_address, re_port):
#             address_port = address + ':' + port
#             print(address_port)

#mayi
headers = {
    'Accept':'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Referer':'http://www.mayidaili.com/free'
}
cookies = {
    'Hm_lvt_dad083bfc015b67e98395a37701615ca':'1560153663,1560327623',
    'Hm_lpvt_dad083bfc015b67e98395a37701615ca':'1560332847',
    'proxy_token':'zgNjGKhB',
}
response = requests.get('http://www.mayidaili.com/free/anonymous/%E9%AB%98%E5%8C%BF/1',headers=headers,cookies=cookies)
find_trs = re.compile('<tr>(.*?)</tr>', re.S)
trs = find_trs.findall(response.text)
for tr in trs:
    find_ip = re.compile('<td>(\d+.\d+.\d+.\d+).*?')
    ip = find_ip.findall(tr)
    find_port_url = re.compile('<img width="80" height="20" class="js-proxy-img" data-uri="(.*?)" />')
    ports_url = find_port_url.findall(tr)
    for port_url in ports_url:
        print(port_url)
        # images = requests.get(port_url,headers=headers,cookies=cookies)
        # with open('y.jpg','wb') as f:
        #     f.write(images.content)
        # #灰度处理
        # image = Image.open('y.jpg')
        # image = image.convert('L')
        # threshold = 80
        # table = []
        # for j in range(256):
        #     if j < threshold:
        #         table.append(0)
        #     else:
        #         table.append(1)
        # image = image.point(table, '1')
        # port = pytesseract.image_to_string(image,config='-psm 7 outputbase digits')
        # print(port)
        # time.sleep(5)