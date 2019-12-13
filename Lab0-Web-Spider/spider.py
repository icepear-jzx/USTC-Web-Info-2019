import urllib.request
import random
import time
from lxml import etree
import json
import socket
import multiprocessing as mp
import os

path = os.path.dirname(os.path.abspath(__file__))

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
    {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}
]


def get_html(url, sleep=True, proxy=None):
    """
    Input url to get HTML.
    Return HTML(str) or None.
    Set sleep=False to skip over sleep step.
    (Default sleep time is 0 ~ 1s)
    Set proxy={"https": "X.X.X.X:XXXX"} to specify a proxy.
    For example, set proxy={} to disable proxy.
    """
    html = None
    put_back = False

    if sleep:
        time.sleep(random.random())

    # If proxy is not specified, pop the first proxy in proxy_list.
    # This proxy will be added back to proxy_list.
    if not proxy:
        while True:
            try:
                proxy = proxy_list.pop(0)
            except:
                continue
            else:
                put_back = True
                break

    # If get an exception, try again.
    # If get HTTPError, there are two cases:
    #   1. The URL doesn't exist (it's possible).
    #   In this case, try again.
    #   2. The proxy is not available any more.
    #   In this case, delete this proxy and try again.
    # To distinguish the two cases, get https://book.douban.com/ to test.
    try:
        # print('Get:', url)
        httpproxy_handler = urllib.request.ProxyHandler(proxy)
        opener = urllib.request.build_opener(httpproxy_handler)
        req = urllib.request.Request(url, headers=random.choice(headers))
        html = opener.open(req, timeout=5).read().decode()
    except urllib.error.HTTPError:
        print('HTTPError:', url)
        try:
            req = urllib.request.Request('https://book.douban.com/', headers=random.choice(headers))
            opener.open(req, timeout=5).read().decode()
        except:
            html = get_html(url, sleep=False)
            print('Delete:', proxy)
            put_back = False
    except Exception as e:
        # print(e, proxy, url)
        html = get_html(url, sleep=False)
    else:
        # print('Success:', url)
        pass
    
    if put_back:
        proxy_list.append(proxy)
    # print('Proxies Remain:', len(proxy_list))

    return html


def get_top250_url():
    """
    Get Top250 books' URLs and save in top250-url.json.
    """
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
    
    with open(path + '/Data/top250-url.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_book_detail(args):
    """
    Get single book's details(bookType, shortRemark, longRemark).
    """
    books, index, max_shortRemark_page, max_longRemark_page = args

    print('Start: No.', index + 1, books[index]['bookName'])

    # Get bookType.
    html = get_html(books[index]['bookURL'])
    if not html:
        print('Get', books[index]['bookName'], 'Error!', 'URL:', books[index]['bookURL'])
        return
    selector = etree.HTML(html)
    books[index]['bookType'] = selector.xpath(
        '//div[@id="db-tags-section"]/div/span/a/text()')
    
    # Get shortRemark.
    shortRemark_list = []
    i = 1
    while True:
        while True:
            shortRemarks = get_html(books[index]['bookURL'] + 'comments/hot?p={}'.format(i))
            try:
                selector = etree.HTML(shortRemarks)
            except:
                continue
            else:
                break
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
            shortRemark_list.append(
                {'id': ids[j], 'content': contents[j], 'starNumber': starNumbers[j],
                    'usefulNumber': usefulNumbers[j]})

        nextButton = selector.xpath(
            '//ul[@class="comment-paginator"]/li[3]/a/@href')
        if nextButton and i < max_shortRemark_page:
            i += 1
        else:
            break

    books[index]['shortRemark'] = shortRemark_list
    
    # Get longRemark.
    longRemark_list = []
    i = 0
    while True:
        longRemarks = get_html(books[index]['bookURL'] + 'reviews?start={}'.format(i))
        while True:
            try:
                selector = etree.HTML(longRemarks)
            except:
                continue
            else:
                break
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

        contents = [""] * len(ids)
        upNumbers = [0] * len(ids)
        downNumbers = [0] * len(ids)
        for review_id in review_ids:
            review = get_html("https://book.douban.com/j/review/" + review_id + "/full", sleep=False)
            while not review:
                review = get_html("https://book.douban.com/j/review/" + review_id + "/full", sleep=False)
            review = json.loads(review)
            contents[review_ids.index(review_id)] = review["html"]
            upNumbers[review_ids.index(review_id)] = review["votes"]["useful_count"]
            downNumbers[review_ids.index(review_id)] = review["votes"]["useless_count"]
        
        for j in range(len(ids)):
            try:
                longRemark_list.append(
                    {'id': ids[j], 'content': contents[j], 'starNumber': starNumbers[j],
                        'usefulNumber': str(upNumbers[j]) + '/' + str(downNumbers[j])})
            except Exception as e:
                print(e, books[index]["bookName"], len(ids), len(contents), len(starNumbers), len(upNumbers), len(downNumbers))

        if nextButton and i < 20 * (max_longRemark_page - 1):
            i += 20
        else:
            break
        
    books[index]['longRemark'] = longRemark_list
    
    print('Finish: No.', index + 1, books[index]['bookName'], 'Proxies Remain:', len(proxy_list))


def get_top250_detail(max_shortRemark_page=1, max_longRemark_page=1):
    """
    Load top250-url.json.
    Get Top250 books' details.
    20 processes in parallel.
    Save in top250-detail.json.
    """
    with open(path + '/Data/top250-url.json', 'r') as f:
        books = json.loads(f.read())
    books = manager.list([manager.dict(book) for book in books])
    args = [(books, i, max_shortRemark_page, max_longRemark_page) for i in range(len(books))]
    pool = mp.Pool(20)
    pool.map(get_book_detail, args)
    pool.close()
    pool.join()

    books = [{key: value for key, value in book.items()} for book in books]
    with open(path + '/Data/top250-detail.json', 'w') as f:
        json.dump(books, f, indent=4, ensure_ascii=False)


def get_tag50_url(args):
    """
    Get all books' URLs in this tag.
    There are only 50 pages shown in single tag, 
    see https://book.douban.com/tag/%E5%A4%96%E5%9B%BD%E6%96%87%E5%AD%A6?start=980
    and https://book.douban.com/tag/%E5%A4%96%E5%9B%BD%E6%96%87%E5%AD%A6?start=1000 .
    The latter doesn't show any books' information.
    Thus we can only get 1000 books' URLs in one tag.
    """
    books_dict, books_list, tag, max_book_num = args
    for i in range(0, 1000, 20):
        if len(books_list) > max_book_num:
            return
        url = 'https://book.douban.com' + urllib.parse.quote(tag) + '?start={}'.format(i)
        html = get_html(url)
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


def get_similar_url(args):
    """
    In any book's page, there are some similar books recommended to readers.
    Get their URLs and add to books_list and books_dict.
    """
    book, books_dict, books_list = args
    html = get_html(book['bookURL'])
    if not html:
        print('Get', book['bookName'], 'Error!', 'URL:', book['bookURL'])
        return
    selector = etree.HTML(html)
    names = selector.xpath('//div[@id="db-rec-section"]//dl/dd/a/text()')
    urls = selector.xpath('//div[@id="db-rec-section"]//dl/dd/a/@href')
    ids = [url[-9:-1] for url in urls]
    for j in range(len(ids)):
        if ids[j] not in books_dict:
            books_dict[ids[j]] = (names[j], urls[j])
            books_list.append({'bookName': names[j], 'bookURL': urls[j]})


def get_all_url(max_book_num=10000):
    """
    Get all books' URL in douban.
    Get all tags from https://book.douban.com/tag/?view=cloud .
    Use get_tag50_url() to get 1000 books in this tag.
    If the number of all these books is less than max_book_num,
    use get_similar_url() to get more.
    """
    books_list = manager.list()
    books_dict = manager.dict()

    # tags
    html = get_html('https://book.douban.com/tag/?view=cloud')
    selector = etree.HTML(html)
    tags = selector.xpath('//table[@class="tagCol"]//td/a/@href')
    args = [(books_dict, books_list, tag, max_book_num) for tag in tags]
    pool = mp.Pool(20)
    pool.map(get_tag50_url, args)
    pool.close()
    pool.join()

    # similar books
    i = 0
    while i < len(books_list) and len(books_list) <= max_book_num:
        print('Book Num:', len(books_list), 'Now:', i + 1)
        book = books_list[i]
        i += 1
        args = (book, books_dict, books_list)
        get_similar_url(args)
    
    books_list = [book for book in books_list]
    with open(path + '/Data/all-url.json', 'w') as f:
        json.dump(books_list, f, indent=4, ensure_ascii=False)
            

if __name__ == "__main__":
    manager = mp.Manager()
    with open(path + '/Data/proxies.json', 'r') as f:
        proxy_list = json.loads(f.read())
    proxy_list = manager.list(proxy_list)
    # get_top250_url()
    get_top250_detail(max_shortRemark_page=1, max_longRemark_page=1)
    get_all_url(max_book_num=20000)

