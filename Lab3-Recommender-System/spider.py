import urllib.request
import random
import time
from lxml import etree
import json
import socket
import multiprocessing as mp
import os
import pickle
from tqdm import tqdm
import http.cookiejar

path = os.path.dirname(os.path.abspath(__file__))

headers = [
    {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'},
    # {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
    # {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
    # {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}
]


def get_html(url):

    html = None
    time.sleep(0.5)

    req = urllib.request.Request(url, headers=random.choice(headers))
    req.add_header('Cookie', 'll="108299"; bid=b3jkq79oW7M; __utmz=30149280.1577110237.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ap_v=0,6.0; __utmz=81379588.1577110298.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); gr_user_id=afd62d3f-3dc7-4100-bf31-ce83c7e75eb5; _vwo_uuid_v2=D7CCA92C731B2D1A658B7015A2E525F42|e3ec03131a10bf0e011667f71b960d47; _pk_ses.100001.3ac3=*; __utma=30149280.670431870.1577110237.1577110237.1577113526.2; __utma=81379588.818571448.1577110298.1577110298.1577113526.2; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=791821d4-c01d-484d-b277-cce6b1fdc8c9; gr_cs1_791821d4-c01d-484d-b277-cce6b1fdc8c9=user_id%3A0; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_791821d4-c01d-484d-b277-cce6b1fdc8c9=true; __utmc=30149280; __utmc=81379588; viewed="1734358_2146498"; __utmt_douban=1; __utmt=1; __yadk_uid=1R66FdJTE2mfpErcqoz2RAEE1Hjr5cHQ; _pk_id.100001.3ac3=cac0a859c54d9f43.1577110298.2.1577114285.1577110785.; __utmb=30149280.17.10.1577113526; __utmb=81379588.17.10.1577113526')
    
    html = urllib.request.urlopen(req).read().decode()

    return html


def get_book(userlist):

    last_user = '1015582'
    
    for user in tqdm(userlist):
        if user <= last_user:
            continue

        rating_dict = {}
        url = 'https://book.douban.com/people/{}/collect?sort=time&start=0&filter=all&mode=list'.format(user)
        html = get_html(url)
        selector = etree.HTML(html)
        num = int(selector.xpath('//span[@class="subject-num"]/text()')[0].split('/')[1])
        start = (num // 30) * 30
        if start > 3000:
            print("jump:", user)
            continue
        
        while True:
            url = 'https://book.douban.com/people/{}/collect?sort=time&start={}&filter=all&mode=list'.format(user, start)
            html = get_html(url)
            selector = etree.HTML(html)
            book_urls = selector.xpath('//div[@class="item-show"]/div[@class="date"]/span/../../div[@class="title"]/a/@href')
            book_ids = [book_url.split('/')[-2] for book_url in book_urls]
            rating_tags = selector.xpath('//div[@class="item-show"]/div[@class="date"]/span/@class')
            ratings = [tag[-3] for tag in rating_tags]
            dates = selector.xpath('//div[@class="item-show"]/div[@class="date"]/span/../../div[@class="date"]/text()')
            dates = [date.strip() for date in dates if '20' in date]
            

            for i in range(len(book_ids)):
                rating_dict[book_ids[i]] = {'rating': ratings[i], 'date': dates[i]}

            start -= 30
            if start < 0 or (dates and dates[0][:4] > '2011'):
                break

        with open(path + '/Data/Book/{}.json'.format(user), 'w') as f:
            json.dump(rating_dict, f, indent=4, ensure_ascii=False)


def get_movie(userlist):

    last_user = '1001637'
    
    for user in tqdm(userlist):
        if user <= last_user:
            continue

        rating_dict = {}
        url = 'https://movie.douban.com/people/{}/collect?sort=time&amp;start=0&amp;filter=all&amp;mode=list&amp;tags_sort=count'.format(user)
        html = get_html(url)
        selector = etree.HTML(html)
        num = int(selector.xpath('//span[@class="subject-num"]/text()')[0].split('/')[1])
        start = (num // 30) * 30
        if start > 3000:
            print("jump:", user)
            continue
        
        while True:
            url = 'https://movie.douban.com/people/{}/collect?sort=time&amp;start={}&amp;filter=all&amp;mode=list&amp;tags_sort=count'.format(user, start)
            html = get_html(url)
            selector = etree.HTML(html)
            book_urls = selector.xpath('//div[@class="item-show"]/div[@class="date"]/span/../../div[@class="title"]/a/@href')
            book_ids = [book_url.split('/')[-2] for book_url in book_urls]
            rating_tags = selector.xpath('//div[@class="item-show"]/div[@class="date"]/span/@class')
            ratings = [tag[-3] for tag in rating_tags]
            dates = selector.xpath('//div[@class="item-show"]/div[@class="date"]/span/../../div[@class="date"]/text()')
            dates = [date.strip() for date in dates if '20' in date]
            

            for i in range(len(book_ids)):
                rating_dict[book_ids[i]] = {'rating': ratings[i], 'date': dates[i]}

            start -= 30
            if start < 0 or (dates and dates[0][:4] > '2011'):
                break

        with open(path + '/Data/Movie/{}.json'.format(user), 'w') as f:
            json.dump(rating_dict, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    
    userlist = pickle.load(open(path + '/Data/userlist.pkl', 'rb'))
    userlist.sort()

    get_movie(userlist)

    