import json
import re
from .utils  import get_page
from pyquery import PyQuery as pq


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

