import requests
import pandas as pd
from scrapy import Selector



class Spider:
    def __init__(self, query_file='Data/test_querys.csv', 
                doc_file='Data/test_docs.csv'):
        query_df = pd.read_csv(query_file)
        doc_df = pd.read_csv(doc_file)
        self.query_dict = {qid: query for qid, query in zip(query_df['query_id'], query_df['query'])}
        self.doc_dict = {doc: did for doc, did in zip(doc_df['doc_title'], doc_df['doc_id'])}

        self.urls = {
            'bing': 'https://cn.bing.com/search?q=query&first=start_number',
            'google': 'https://www.google.com/search?q=query&start=start_number',
            'baidu': 'https://www.baidu.com/s?wd=query&pn=start_number',
        }
        self.xpaths = {
            'google': '//*[@id="rso"]/div/div/div[number]/div/div/div[1]/a/h3/text()',
            'bing': '//*[@id="b_results"]/li[number]/div/h2/a//text()',
            'baidu': '//*[@id="number"]/h3/a//text()',
        }
        self.headers = headersParameters = {
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/6.1 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }


    def search(self, qid, engine='bing'):
        query = self.query_dict[qid]
        urls = self.urls
        xpaths = self.xpaths

        answers = []
        for i in range(0, 100, 10):
            url = urls[engine].replace('query', query).replace('start_number', str(i))
            response = requests.get(url, headers=self.headers, timeout=2000)
            select = Selector(text=response.text)
            for j in range(10):
                xpath = xpaths[engine].replace('number', str(j + 1))
                title = ''.join(select.xpath(xpath).extract())
                title = title.replace('？', '?')
                try:
                    answers.append(self.doc_dict[title])
                    print(title)
                except:
                    pass


Spider().search('q481010', engine='baidu')


