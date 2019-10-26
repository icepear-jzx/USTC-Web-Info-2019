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
        # get bookType
        html = scraper.get(book['bookURL'])
        selector = etree.HTML(html.content)
        book['bookType'] = selector.xpath(
            '//div[@id="db-tags-section"]/div/span/a/text()')

        # get shortRemark
        book['shortRemark'] = []
        i = 1
        while True:
            shortRemarks = scraper.get(
                book['bookURL'] + 'comments/hot?p={}'.format(i))
            selector = etree.HTML(shortRemarks.content)
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
                print('Finish comments page', i)
                i += 1
            else:
                break

        # get longRemark
        book['longRemark'] = []
        i = 0
        while True:
            shortRemarks = scraper.get(
                book['bookURL'] + 'reviews?start={}'.format(i))
            selector = etree.HTML(shortRemarks.content)
            nextButton = selector.xpath(
                '//div[@class="paginator"]/span[@class="next"]/a/@href')
            ids = selector.xpath(
                '//header[@class="main-hd"]/a[@class="name"]/text()')
            urls = selector.xpath(
                '//div[@class="main-bd"]/h2/a/@href')
            starClasses = selector.xpath(
                '//header[@class="main-hd"]/span[1]/@class')
            starNumbers = [starClass.split()[0][-2]
                           for starClass in starClasses]
            upNumbers = selector.xpath(
                '//div[@class="main-bd"]//a[@class="action-btn up"]/span/text()')
            downNumbers = selector.xpath(
                '//div[@class="main-bd"]//a[@class="action-btn down"]/span/text()')
            # print(ids, upNumbers, downNumbers)
            contents = []
            for url in urls:
                review = scraper.get(url)
                selector = etree.HTML(review.content)
                content = selector.xpath(
                    """//div[@id="link-report"]/div[@class="review-content clearfix"]/text()|
                    //div[@id="link-report"]/div[@class="review-content clearfix"]/p/text()""")
                contents.append(content)

            for j in range(len(ids)):
                book['longRemark'].append(
                    {'id': ids[j], 'content': contents[j], 'starNumber': starNumbers[j],
                     'usefulNumber': upNumbers[j].strip() + '/' + downNumbers[j].strip()})

            if nextButton and i < 0:
                print('Finish reviews number', i)
                i += 20
            else:
                break
        # only 1 book
        break

    f = open('top250-detail.json', 'w')
    json.dump(books, f, indent=4)


get_top250_detail()
f = open('top250-detail.json', 'r')
books = json.loads(f.read())
print(books[0])
