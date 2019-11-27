import urllib.request
import time
import random
from lxml import etree
import json
from tqdm import tqdm
import pandas as pd


headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
    {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}
]


def get_html(url):
    time.sleep(0.1)

    httpproxy_handler = urllib.request.ProxyHandler({})
    opener = urllib.request.build_opener(httpproxy_handler)
    req = urllib.request.Request(url, headers=random.choice(headers))
    html = opener.open(req, timeout=5).read().decode()

    return html


data = pd.read_csv('Lab1-Search-Engine/Data/test_querys.csv')

querys = {}

for i, row in tqdm(list(data.iterrows())):

    # html = get_html('https://www.baidu.com/s?wd={}'.format(urllib.parse.quote(row['query'])))
    
    # with open('Lab1-Search-Engine/Data/HTML/{}.html'.format(row['query_id']), 'w') as f:
    #     f.write(html)
    try:
        with open('Lab1-Search-Engine/Data/HTML/' + row['query_id'] + '.html') as f:
            html = f.read()
        selector = etree.HTML(html)
        titles = selector.xpath('//div[@id="content_left"]/div/h3/a//text()')    
        querys[row['query_id']] = " ".join(titles)
    except:
        pass
        # try:
        #     html = get_html('https://www.baidu.com/s?wd={}'.format(urllib.parse.quote(row['query'])))
        #     with open('Lab1-Search-Engine/Data/HTML/{}.html'.format(row['query_id']), 'w') as f:
        #         f.write(html)
        # except:
        #     pass

with open('Lab1-Search-Engine/Data/querys_spider.json', 'w') as f:
    json.dump(querys, f, indent=4, ensure_ascii=False)
