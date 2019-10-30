import urllib.request
import random
import time
from lxml import etree
import json
import socket
import multiprocessing as mp


headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
    {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}
]


def get_html(url, sleep=True, sleep_time=1):
    html = None

    if sleep:
        time.sleep(random.random() * sleep_time)

    try:
        print('Get:', url)
        req = urllib.request.Request(url, headers=random.choice(headers))
        html = urllib.request.urlopen(req, timeout=3).read().decode()
    except socket.timeout:
        print('Timeout:', url)
        print('Retry:', url)
        html = get_html(url)
    except urllib.error.HTTPError:
        print('Error:', url)
    else:
        print('Success:', url)
    
    return html


def get_top250_url():
    data = []

    for i in range(0, 250, 25):
        url = "https://book.douban.com/top250?start={}".format(i)

        html = get_html(url)
        if not html:
            continue

        selector = etree.HTML(html)
        names = selector.xpath('//div[@class="pl2"]/a/@title')
        urls = selector.xpath('//div[@class="pl2"]/a/@href')
        for j in range(25):
            data.append({"bookName": names[j], "bookURL": urls[j]})

        print('Finish:', url)

    with open('top250-url.json', 'w') as f:
        json.dump(data, f, indent=4)
    
    with open('top250-url-gbk.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_top250_detail():
    with open('top250-url.json', 'r') as f:
        books = json.loads(f.read())

    for book in books:
        # get bookType
        html = get_html(book['bookURL'])
        if not html:
            print('Get', book['bookName'], 'Error!', 'URL:', book['bookURL'])
            continue
        selector = etree.HTML(html)
        book['bookType'] = selector.xpath(
            '//div[@id="db-tags-section"]/div/span/a/text()')

        # get shortRemark
        book['shortRemark'] = []
        i = 1
        while True:
            shortRemarks = get_html(book['bookURL'] + 'comments/hot?p={}'.format(i))
            selector = etree.HTML(shortRemarks)
            ids = selector.xpath(
                '//div[@class="comment"]//span[@class="comment-info"]/a/text()')
            starClasses = selector.xpath(
                """//div[@class="comment"]//span[@class="comment-info"]/span/text()|
                //div[@class="comment"]//span[@class="comment-info"]/span/@class""")
            starNumbers = ["0"] * len(ids)
            j = k = 0
            while j < len(ids):
                if len(starClasses[k]) != 10:
                    starNumbers[j] = starClasses[k].split()[1][-2]
                    j += 1
                    k += 2
                else:
                    j += 1
                    k += 1

            usefulNumbers = selector.xpath(
                '//div[@class="comment"]//span[@class="comment-vote"]/span/text()')
            contents = selector.xpath(
                '//div[@class="comment"]//p[@class="comment-content"]/span/text()')

            for j in range(len(ids)):
                book['shortRemark'].append(
                    {'id': ids[j], 'content': contents[j], 'starNumber': starNumbers[j],
                     'usefulNumber': usefulNumbers[j]})

            nextButton = selector.xpath(
                '//ul[@class="comment-paginator"]/li[3]/a/@href')
            if nextButton and i < 1:
                i += 1
            else:
                break

        # get longRemark
        book['longRemark'] = []
        i = 0
        while True:
            longRemarks = get_html(book['bookURL'] + 'reviews?start={}'.format(i))
            selector = etree.HTML(longRemarks)
            nextButton = selector.xpath(
                '//div[@class="paginator"]/span[@class="next"]/a/@href')
            ids = selector.xpath(
                '//header[@class="main-hd"]/a[@class="name"]/text()')
            review_ids = selector.xpath(
                '//div[@class="review-list  "]/div/@data-cid')
            starClasses = selector.xpath(
                '//header[@class="main-hd"]/span[1]/@class')
            starNumbers = [starClass.split()[0][-2]
                           for starClass in starClasses]
            upNumbers = selector.xpath(
                '//div[@class="main-bd"]//a[@class="action-btn up"]/span/text()')
            downNumbers = selector.xpath(
                '//div[@class="main-bd"]//a[@class="action-btn down"]/span/text()')

            contents = []
            for review_id in review_ids:
                review = get_html("https://book.douban.com/j/review/" + review_id + "/full", sleep=False)
                review = json.loads(review)
                contents.append(review["html"])

            for j in range(len(ids)):
                book['longRemark'].append(
                    {'id': ids[j], 'content': contents[j], 'starNumber': starNumbers[j],
                     'usefulNumber': upNumbers[j].strip() + '/' + downNumbers[j].strip()})
            
            if nextButton and i < 0:
                i += 20
            else:
                break
        
        print('Finish: No.', books.index(book) + 1, book['bookName'])

    with open('top250-detail.json', 'w') as f:
        json.dump(books, f, indent=4)

    with open('top250-detail-gbk.json', 'w') as f:
        json.dump(books, f, indent=4, ensure_ascii=False)


def get_tag50_url(books_dict, books_list, tag, max_book_num):
    for i in range(0, 1000, 20):
        url = 'https://book.douban.com' + urllib.parse.quote(tag) + '?start={}'.format(i)
        html = get_html(url, sleep_time=5)
        if not html:
            continue
        selector = etree.HTML(html)
        names = selector.xpath('//li[@class="subject-item"]/div[@class="info"]/h2/a/@title')
        urls = selector.xpath('//li[@class="subject-item"]/div[@class="info"]/h2/a/@href')
        ids = [url[-9:-1] for url in urls]
        
        for j in range(len(ids)):
            if ids[j] not in books_dict:
                books_dict[ids[j]] = (names[j], urls[j])
                books_list.append({'bookName': names[j], 'bookURL': urls[j]})
        print('Book Num:', len(books_list))
        if len(books_list) > max_book_num:
            break


def get_all_url(max_book_num=10000):
    manager = mp.Manager()
    books_list = manager.list()
    books_dict = manager.dict()
    jobs = []

    # tags
    html = get_html('https://book.douban.com/tag/?view=cloud')
    selector = etree.HTML(html)
    tags = selector.xpath('//table[@class="tagCol"]//td/a/@href')
    args = [(books_dict, books_list, tag, max_book_num) for tag in tags]
    pool = mp.Pool(3)
    pool.map_async(get_tag50_url, args)
    pool.close()
    pool.join()

    # similar books
    i = 0
    while i < len(books_list) and len(books_list) <= max_book_num:
        print('Book Num:', len(books_list), 'Now:', i + 1)
        book = books_list[i]
        i += 1
        html = get_html(book['bookURL'])
        if not html:
            print('Get', book['bookName'], 'Error!', 'URL:', book['bookURL'])
            continue
        selector = etree.HTML(html)
        names = selector.xpath('//div[@id="db-rec-section"]//dl/dd/a/text()')
        urls = selector.xpath('//div[@id="db-rec-section"]//dl/dd/a/@href')
        ids = [url[-9:-1] for url in urls]
        for j in range(len(ids)):
            if ids[j] not in books_dict:
                books_dict[ids[j]] = (names[j], urls[j])
                books_list.append({'bookName': names[j], 'bookURL': urls[j]})
    
    books_list = [book for book in books_list]
    with open('all-url.json', 'w') as f:
        json.dump(books_list, f, indent=4)
    
    with open('all-url-gbk.json', 'w') as f:
        json.dump(books_list, f, indent=4, ensure_ascii=False)
            
        
# get_top250_url()
# get_top250_detail()
# with open('top250-url.json', 'r') as f:
#     books = json.loads(f.read())
# print(books[0])
get_all_url(max_book_num=1000)

