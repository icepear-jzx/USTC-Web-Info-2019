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
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
    {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}
]


def get_html(url, sleep=True, proxy=None):

    html = None
    put_back = False

    if sleep:
        time.sleep(random.random())

    if not proxy:
        while True:
            try:
                proxy = proxy_list.pop(0)
            except:
                continue
            else:
                put_back = True
                break

    try:
        # print('Get:', url)
        cookie_jar = http.cookiejar.CookieJar()
        cookie_handler = urllib.request.HTTPCookieProcessor(cookie_jar)
        proxy_handler = urllib.request.ProxyHandler(proxy)

        opener = urllib.request.build_opener(proxy_handler, cookie_handler)
        header = random.choice(headers)

        req = urllib.request.Request('https://book.douban.com/', headers=header)
        html = opener.open(req, timeout=5)

        cookie = ""
        for item in cookie_jar:
            cookie += "{}={};".format(item.name, item.value)
        
        header['Cookie'] = cookie

        req = urllib.request.Request(url, headers=header)
        html = opener.open(req, timeout=5).read().decode()

    except urllib.error.HTTPError as e:
        # print('HTTPError:', url, e)
        if '404' in str(e):
            # print('404:', url)
            html = None
        elif '403' in str(e):
            # print('403:', url)
            print('Delete:', proxy)
            put_back = False
            html = get_html(url, sleep=False)
    except Exception as e:
        # print(e, proxy, url)
        if random.random() < 0.01:
            print('Delete:', proxy)
            put_back = False
        html = get_html(url, sleep=False)
    else:
        # print('Success:', url)
        pass
    
    if put_back:
        proxy_list.append(proxy)
    else:
        print('Proxies Remain:', len(proxy_list))

    return html


def get_book(args):

    user, = args
    
    rating_dict = {}
    url = 'https://book.douban.com/people/{}/collect?sort=time&start=0&filter=all&mode=list'.format(user)
    html = get_html(url, sleep=False)
    if not html:
        print("jump:", user)
        return
    if "paginator" not in html:
        # print('Spider Trap:', url)
        print("jump:", user)
        return

    selector = etree.HTML(html)
    num = int(selector.xpath('//span[@class="subject-num"]/text()')[0].split('/')[1])
    start = (num // 30) * 30
    if start > 5000:
        print("jump:", user)
        continue
    
    while True:
        url = 'https://book.douban.com/people/{}/collect?sort=time&start={}&filter=all&mode=list'.format(user, start)
        html = get_html(url, sleep=False)
        while "paginator" not in html:
            # print('Spider Trap:', url)
            html = get_html(url, sleep=False)
        selector = etree.HTML(html)
        book_all_urls = selector.xpath('//div[@class="item-show"]/div[@class="title"]/a/@href')
        book_all_ids = [book_url.split('/')[-2] for book_url in book_all_urls]
        book_urls = selector.xpath('//div[@class="item-show"]/div[@class="date"]/span/../../div[@class="title"]/a/@href')
        book_ids = [book_url.split('/')[-2] for book_url in book_urls]
        rating_tags = selector.xpath('//div[@class="item-show"]/div[@class="date"]/span/@class')
        ratings = [tag[-3] for tag in rating_tags]
        dates = selector.xpath('//div[@class="item-show"]/div[@class="date"]/span/../../div[@class="date"]/text()')
        dates = [date.strip() for date in dates if '20' in date]
        

        for i in range(len(book_ids)):
            rating_dict[book_ids[i]] = {'rating': ratings[i], 'date': dates[i]}

        for book_id in book_all_ids:
            if book_id not in book_ids:
                rating_dict[book_id] = {'rating': "0", 'date': "NaN"}

        start -= 30
        if start < 0 or (dates and dates[0][:4] > '2011'):
            break

    with open(path + '/Data/Book/{}.json'.format(user), 'w') as f:
        json.dump(rating_dict, f, indent=4, ensure_ascii=False)

    print('Finish:', user)
    

def get_books(userlist, userlist_got):

    args = [(user, ) for user in userlist if user not in userlist_got]
    pool = mp.Pool(30)
    pool.map(get_movie, args)
    pool.close()
    pool.join()


def get_movie(args):
    user, = args
    # print('Start:', user)

    rating_dict = {}
    url = 'https://movie.douban.com/people/{}/collect?sort=time&amp;start=0&amp;filter=all&amp;mode=list&amp;tags_sort=count'.format(user)
    html = get_html(url, sleep=False)
    if not html:
        print("jump:", user)
        return
    if "paginator" not in html:
        # print('Spider Trap:', url)
        print("jump:", user)
        return
    
    selector = etree.HTML(html)
    num = int(selector.xpath('//span[@class="subject-num"]/text()')[0].split('/')[1])
    start = (num // 30) * 30
    if start > 5000:
        print("jump:", user)
        return
    
    while True:
        url = 'https://movie.douban.com/people/{}/collect?sort=time&amp;start={}&amp;filter=all&amp;mode=list&amp;tags_sort=count'.format(user, start)
        html = get_html(url, sleep=False) # html != None
        while "paginator" not in html:
            # print('Spider Trap:', url)
            html = get_html(url, sleep=False)
        selector = etree.HTML(html)
        movie_all_urls = selector.xpath('//div[@class="item-show"]/div[@class="title"]/a/@href')
        movie_all_ids = [movie_url.split('/')[-2] for movie_url in movie_all_urls]
        movie_urls = selector.xpath('//div[@class="item-show"]/div[@class="date"]/span/../../div[@class="title"]/a/@href')
        movie_ids = [movie_url.split('/')[-2] for movie_url in movie_urls]
        rating_tags = selector.xpath('//div[@class="item-show"]/div[@class="date"]/span/@class')
        ratings = [tag[-3] for tag in rating_tags]
        dates = selector.xpath('//div[@class="item-show"]/div[@class="date"]/span/../../div[@class="date"]/text()')
        dates = [date.strip() for date in dates if '20' in date]
        

        for i in range(len(movie_ids)):
            rating_dict[movie_ids[i]] = {'rating': ratings[i], 'date': dates[i]}
        
        for movie_id in movie_all_ids:
            if movie_id not in movie_ids:
                rating_dict[movie_id] = {'rating': "0", 'date': "NaN"}

        start -= 30
        if start < 0 or (dates and dates[0][:4] > '2011'):
            break

    with open(path + '/Data/Movie/{}.json'.format(user), 'w') as f:
        json.dump(rating_dict, f, indent=4, ensure_ascii=False)
    
    print('Finish:', user)


def get_movies(userlist, userlist_got):

    args = [(user, ) for user in userlist if user not in userlist_got]
    pool = mp.Pool(30)
    pool.map(get_movie, args)
    pool.close()
    pool.join()


if __name__ == "__main__":

    manager = mp.Manager()
    with open(path + '/Data/proxies.json', 'r') as f:
        proxy_list = json.loads(f.read())
    proxy_list = manager.list(proxy_list)
    
    userlist = pickle.load(open(path + '/Data/userlist.pkl', 'rb'))
    userlist.sort()

    userlist_got = [filename[:-5] for filename in os.listdir(path + '/Data/Movie')]
    input(str(len(userlist_got)) + '/' + str(len(userlist)))
    get_movies(userlist, userlist_got)

    # get_books(userlist, book_last_user)

    