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


def get_html(url, sleep=True):
    html = None
    if sleep:
        time.sleep(random.random())

    try:
        print('Get:', url)
        req = urllib.request.Request(url, headers=random.choice(headers))
        html = urllib.request.urlopen(req).read().decode()
        print('Success:', url)
    except:
        print('Error:', url)
    
    return html


def get_top250_url():
    data = []

    for i in range(0, 250, 25):
        url = "https://book.douban.com/top250?start={}".format(i)

        html = None
        while not html:
            html = get_html(url)

        selector = etree.HTML(html)
        names = selector.xpath('//div[@class="pl2"]/a/@title')
        urls = selector.xpath('//div[@class="pl2"]/a/@href')
        for j in range(25):
            data.append({"bookName": names[j], "bookURL": urls[j]})

        print('Finish:', url)

    with open('top250-url.json', 'w') as f:
        json.dump(data, f, indent=4)


def get_top250_detail():
    with open('top250-url.json', 'r') as f:
        books = json.loads(f.read())

    for book in books:
        # get bookType
        html = get_html(book['bookURL'])
        while not html:
            print('Get', book['bookName'], 'Error!', 'URL:', book['bookURL'])
            input('Input Enter to continue:')
            continue
        selector = etree.HTML(html)
        book['bookType'] = selector.xpath(
            '//div[@id="db-tags-section"]/div/span/a/text()')

        # get shortRemark
        book['shortRemark'] = []
        i = 1
        while True:
            shortRemarks = None
            while not shortRemarks:
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
            longRemarks = None
            while not longRemarks:
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
                review = None
                while not review:
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
        
        print('Finish: book', books.index(book))

    with open('top250-detail.json', 'w') as f:
        json.dump(books, f, indent=4)


get_top250_detail()
# f = open('top250-detail.json', 'r')
# books = json.loads(f.read())
# print(books[0])
# get_top250_url()
