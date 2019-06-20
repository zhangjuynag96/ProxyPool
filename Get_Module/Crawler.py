import json
import re
from .utils import get_page
from pyquery import PyQuery as pq
import requests
import tesserocr
from PIL import Image
import pytesseract
from lxml import etree
from selenium import webdriver
import PIL
import numpy as np
from bs4 import BeautifulSoup as bs
import time

class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print('成功获取到代理', proxy)
            proxies.append(proxy)
        return proxies

    def crawl_mimvp(self):
        """
        获取米扑代理
        :return: 代理
        """
        response = get_page('https://proxy.mimvp.com/free.php?proxy=in_hp')
        pattern = re.compile(
            "<td class='tbl-proxy-ip' style='text-align: left;'>(\d+.\d+.\d+.\d+)</td><td class='tbl-proxy-port'><img src=(.*?) /></td><td class='tbl-proxy-type'")
        result = pattern.findall(response)
        for i in result:
            url = 'https://proxy.mimvp.com/' + i[1]
            images = requests.get(url)
            with open('x.jpg', 'wb') as f:
                f.write(images.content)
            image = Image.open('x.jpg')
            image = image.convert('L')
            threshold = 80
            table = []
            for j in range(256):
                if j < threshold:
                    table.append(0)
                else:
                    table.append(1)
            image = image.point(table, '1')
            # port = tesserocr.image_to_text(image)
            port = pytesseract.image_to_string(image, config='-psm 7 outputbase digits')
            if port == '3333':
                port = '9999'
            yield ':'.join([i[0], port])


    # def crawl_xici(self):
    #     """
    #     获取西刺代理
    #     :param page: 页码
    #     :return: 代理
    #     """
    #     for page in range(1, 10):
    #         response = get_page('https://www.xicidaili.com/nn/{page}'.format(page=page))
    #         find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
    #         trs = find_trs.findall(response)
    #         for tr in trs:
    #             find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
    #             re_ip_address = find_ip.findall(tr)
    #             find_port = re.compile('<td>(\d+)</td>')
    #             re_port = find_port.findall(tr)
    #             for address, port in zip(re_ip_address, re_port):
    #                 address_port = address + ':' + port
    #                 yield address_port.replace(' ', '')
    #
    # def crawl_mayi(self):
    #     """
    #     获取蚂蚁代理
    #     :param page: 页码
    #     :return: 代理
    #     """
    #     #基础设置
    #     options = webdriver.ChromeOptions()
    #     options.add_argument("--headless")
    #     options.add_argument("--disable-gpu")
    #     driver = webdriver.Chrome(options=options)
    #     headers = {
    #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    #         'Accept-Encoding': 'gzip, deflate',
    #         'Accept-Language': 'zh-CN,zh;q=0.9',
    #         'Cache-Control': 'max-age=0',
    #         'Connection': 'keep-alive',
    #         'Cookie': 'Hm_lvt_dad083bfc015b67e98395a37701615ca=1554796082; JSESSIONID=C6FF5039054C48DCFDB16B97F1174DA5; proxy_token=xACHriPa; Hm_lpvt_dad083bfc015b67e98395a37701615ca=1554808505',
    #         'Host': 'www.mayidaili.com',
    #         'Upgrade-Insecure-Requests': '1',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    #
    #     #主体爬虫部分
    #     url = "http://www.mayidaili.com/free/{page}"
    #     session = requests.Session()
    #     for page in range(1, 10):
    #         url_ = url.format(page=page)
    #         print(url_.center(100, "*"))
    #         response = driver.get(url_)
    #         content = driver.page_source
    #         html = etree.HTML(content)
    #         ips = list(map(lambda obj: obj.strip(), html.xpath("//tr/td[1]/text()")))
    #         port_imgs = html.xpath("//tr/td[2]/img[@class='js-proxy-img']/@src")
    #         # 这个是遇到的一个坑，使用浏览器产生的headers时，status_code是成功的
    #         # 但是图片是下载不到的，最后用这种方式搞定。
    #         cookies = driver.get_cookies()
    #         s = ""
    #         for cookie in cookies:
    #             s += "{}={}; ".format(cookie['name'], cookie['value'])
    #         s = s[:-2]
    #         headers["Cookie"] = s
    #         ports = []
    #         for img in port_imgs:
    #             images = requests.get(img, headers=headers)
    #             if images.status_code == 200:
    #                 with open("test.jpg", 'wb') as file:
    #                     for chunk in images.iter_content(128):
    #                         file.write(chunk)
    #             #使用numpy与pytesseract解决图片识别
    #             img = PIL.Image.open('test.jpg')
    #             img = np.array(img)
    #             img_ = np.array(list(map(lambda obj: obj if obj < 1 else 255, img.ravel()))).reshape(img.shape)
    #             img = PIL.Image.fromarray(img_.astype(np.uint8))
    #             port = pytesseract.image_to_string(img, config='-psm 8 outputbase digits')
    #             port_l = list(port)
    #             for i in range(0, len(port_l)):
    #                 if port_l[i] == '5':
    #                     port_l[i] = '8'
    #             x = ''.join(port_l)
    #             if x == '2128':
    #                 ports.append('3128')
    #             elif x == '2129':
    #                 ports.append('3129')
    #             else:
    #                 ports.append(x)
    #         for ip, port in zip(ips, ports):
    #             address_port = ip + ':' + port
    #             yield address_port.replace(' ', '')

    def crawl_kuaidaili(self):
        """
        获取快代理
        :param page: 页码
        :return: 代理
        """
        for page in range(1, 10):
            response = get_page('https://www.kuaidaili.com/free/inha/{page}/'.format(page=page))
            time.sleep(2)
            soup = bs(response, 'lxml')
            addresses = []
            ports = []
            for tr in soup.find_all(name='tr'):
                x = []
                for td in tr.find_all(name='td'):
                    x.append(td.string)
                if len(x) > 0:
                    addresses.append(x[0])
                    ports.append(x[1])
                else:
                    pass
            for address, port in zip(addresses, ports):
                address_port = address + ':' + port
                yield address_port.replace(' ', '')

    def crawl_ip3366_free(self):
        """
        获取云代理免费代理界面
        :param page: 页码
        :return: 代理
        """
        for page in range(1, 7):
            start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)
            html = get_page(start_url)
            ip_address = re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            # \s * 匹配空格，起到换行作用
            re_ip_address = ip_address.findall(html)
            for address, port in re_ip_address:
                result = address + ':' + port
                yield result.replace(' ', '')

    def crawl_ip3366_web(self):
        """
        获取云代理首页
        :param page: 页码
        :return: 代理
        """
        for page in range(1, 7):
            start_url = 'http://www.ip3366.net/?stype=1&page={}'.format(page)
            html = get_page(start_url)
            if html:
                find_tr = re.compile('<tr>(.*?)</tr>', re.S)
                trs = find_tr.findall(html)
                for s in range(1, len(trs)):
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(trs[s])
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(trs[s])
                    for address, port in zip(re_ip_address, re_port):
                        address_port = address + ':' + port
                        yield address_port.replace(' ', '')

    def crawl_daili66(self, page_count=4):
        """
        获取代理66
        :param page_count: 页码
        :return: 代理
        """
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

