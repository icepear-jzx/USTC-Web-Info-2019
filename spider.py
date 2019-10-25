import cfscrape
from lxml import etree
import json


def get_top250_url():
    data = []
    scraper = cfscrape.create_scraper()

    for i in range(0, 250, 25):
        html = scraper.get("https://book.douban.com/top250?start={}".format(i))
        selector = etree.HTML(html.content)
        names = selector.xpath('//div[@class="pl2"]/a/@title')
        urls = selector.xpath('//div[@class="pl2"]/a/@href')
        for j in range(25):
            data.append({"bookName": names[j], "bookURL": urls[j]})

    f = open('top250-url.json', 'w')
    json.dump(data, f, indent=4)


def get_top250_detail():
    f = open('top250-url.json', 'r')
    books = json.loads(f.read())
    scraper = cfscrape.create_scraper()
    for book in books:
        shortRemarks = scraper.get(book['bookURL'] + 'comments')
        selector = etree.HTML(shortRemarks.content)


        # longRemarks = scraper.get(book['bookURL'] + 'reviews')
        


