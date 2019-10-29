import urllib.request
import random
import time
from lxml import etree
import json


headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
    {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}
]


def book_spider():
    data = []

    for i in range(0, 250, 25):
        url = "https://book.douban.com/top250?start={}".format(i)
        time.sleep(random.random() * 5)

        try:
            req = urllib.request.Request(url, headers=random.choice(headers))
            html = urllib.request.urlopen(req).read().decode()
        except:
            print('Error:', url)
            continue

        selector = etree.HTML(html)
        names = selector.xpath('//div[@class="pl2"]/a/@title')
        urls = selector.xpath('//div[@class="pl2"]/a/@href')
        for j in range(25):
            data.append({"bookName": names[j], "bookURL": urls[j]})

        print('Finish:', url)

    with open('top250-url-test.json', 'w') as f:
        json.dump(data, f, indent=4)


book_spider()
