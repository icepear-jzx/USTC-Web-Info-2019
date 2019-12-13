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


def test_proxy(proxy):
    try:
        print('Proxy:', proxy)
        httpproxy_handler = urllib.request.ProxyHandler(proxy)
        opener = urllib.request.build_opener(httpproxy_handler)
        req = urllib.request.Request(url, headers=random.choice(headers))
        for _ in range(5):
            html = opener.open(req, timeout=5).read().decode()
    except:
        print('Fail.')
    else:
        print('Success.')
        proxy_list.append(proxy)


proxy_list = mp.Manager().list()
url = 'https://book.douban.com/'
with open(path + '/Data/proxies.txt', 'r') as f:
    proxy_txt = f.read().split('\n')
proxies = [{"https": proxy} for proxy in proxy_txt]
# with open('proxies.json', 'r') as f:
#     proxies = json.loads(f.read())

pool = mp.Pool(200)
pool.map(test_proxy, proxies)
pool.close()
pool.join()

proxy_list = [proxy for proxy in proxy_list]
with open(path + '/Data/proxies.json', 'w') as f:
    json.dump(proxy_list, f, indent=4)
