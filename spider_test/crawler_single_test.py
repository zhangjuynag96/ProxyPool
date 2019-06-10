import requests
import re
from pyquery import PyQuery as pq
from  proxypool.utils import get_page
import tesserocr
from PIL import Image
import pytesseract


# mimvp
def crawler_mimvp():
    response = get_page('https://proxy.mimvp.com/freeopen.php?proxy=in_hp&sort=&page=1')
    pattern = re.compile("<td class='tbl-proxy-ip' style='text-align: left;'>(\d+.\d+.\d+.\d+)</td><td class='tbl-proxy-port'><img src=(.*?) /></td><td class='tbl-proxy-type'")
    result = pattern.findall(response)
    for i in result:
        url = 'https://proxy.mimvp.com/' + i[1]
        images = requests.get(url)
        with open('x.jpg','wb') as f:
            f.write(images.content)
        #灰度处理
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
        port = pytesseract.image_to_string(image,config='-psm 7 outputbase digits')
        if port == '3333':
            port = '9999'


if __name__ == '__main__':
    crawler_mimvp()
