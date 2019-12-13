import pkuseg
import pandas as pd
from collections import Counter
import json
from tqdm import tqdm
import jieba 
import jieba.analyse
import argparse
import os


path = os.path.dirname(os.path.abspath(__file__))


def pkuseg_tokenizer(title_weight=10):
    seg = pkuseg.pkuseg()
    stopword = ['~', '`', '!', '@', '#', '$', '%', '^', '&', '*',
                '(', ')', '_', '-', '+', '=', '[', ']', '{', '}', '\\', '|',
                ';', ':', '\'', '"', ',', '<', '>', '.', '/', '?']
    english = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
                'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    connect = [':', '.', '-']
    numbers = list('1234567890')

    data = pd.read_csv(path+'/Data/test_docs.csv')
    token_count = []

    for i, row in tqdm(list(data.iterrows())):
        if str(row['content']) == 'nan' or str(row['doc_title']) == 'nan':
            continue
        else:
            text = row['doc_title'] * title_weight + row['content']
        
        text = list(text)
        for j in range(len(text)):
            if text[j] in english:
                text[j] = text[j].lower()
        j = 1
        while j < len(text):
            if text[j] in stopword:
                try:
                    if text[j] in connect and text[j-1] in numbers and text[j+1] in numbers:
                        pass
                    else:
                        text[j] = ' '
                except: text[j] = ' '
            
            if text[j] in english and text[j-1] not in english:
                text.insert(j, ' ')
                j += 1
            elif text[j-1] in english and text[j] not in english:
                text.insert(j, ' ')
                j += 1
            j += 1

        text = ''.join(text)

        tokens = seg.cut(text)

        tokens = [token for token in tokens if token not in stopword]

        tokens = Counter(tokens)
        token_count.append({
            'doc_id': row['doc_id'],
            'doc_url': row['doc_url'],
            'doc_title': row['doc_title'],
            'tokens': tokens
        })

    with open(path+'/Data/docs_token_pkuseg.json', 'w') as f:
        json.dump(token_count, f, indent=4, ensure_ascii=False)

    data = pd.read_csv(path+'/Data/test_querys.csv')
    token_count = {}

    for i, row in tqdm(list(data.iterrows())):
        text = row['query']
        text = list(text)
        if row['query_id'] == 'q370116':    # 朱自清
            text.insert(3, ' ')
        elif row['query_id'] == 'q262135':  # 家乡的桥课件
            text.insert(4, ' ')
        elif row['query_id'] == 'q23086':   # 清明节黑板报资料
            text.append('手抄报')
        elif row['query_id'] == 'q321561':  # 枪神纪道具城
            text = ['枪神纪道聚城']
            text.append('《道聚城》')
            text.append('《枪神纪》')
        
        for j in range(len(text)):
            if text[j] in english:
                text[j] = text[j].lower()

        j = 1
        while j < len(text):
            if text[j] in stopword and text[j] not in connect:
                text[j] = ' '
            if text[j] in english and text[j-1] not in english:
                text[j] = text[j].lower()
                text.insert(j, ' ')
                j += 1
            elif text[j-1] in english and text[j] not in english:
                text[j-1] = text[j-1].lower()
                text.insert(j, ' ')
                j += 1
            j += 1

        text = ''.join(text)

        tokens = seg.cut(text)

        tokens = [token for token, tag in tokens 
            if tag not in stopword_tags and token not in stopword]
        tokens = Counter(tokens)
        token_count[row['query_id']] = {
            'query_id': row['query_id'],
            'query': row['query'],
            'tokens': tokens
        }

    with open(path+'/Data/querys_token_pkuseg.json', 'w') as f:
        json.dump(token_count, f, indent=4, ensure_ascii=False)


def jieba_tokenizer(title_weight=10):
    jieba.add_word('道聚城')
    jieba.add_word('枪神纪')
    jieba.add_word('朱自清')
    jieba.add_word('刘诗诗')
    jieba.add_word('床吻戏')
    jieba.add_word('硫酸根')
    jieba.add_word('口算')
    jieba.add_word('化工制图')
    jieba.add_word('头像领取中心')
    jieba.add_word('开不了机')
    jieba.add_word('李蒽熙')
    jieba.add_word('韩安冉')
    jieba.add_word('画法几何及工程制图')
    jieba.suggest_freq('幼儿园', True)
    jieba.suggest_freq('家长会', True)
    jieba.suggest_freq('中班', True)
    jieba.suggest_freq('三角形', True)
    jieba.suggest_freq('盐城赶集网', True)
    jieba.suggest_freq('百度知道', True)
    jieba.suggest_freq('百度文库', True)
    jieba.suggest_freq('下载器', True)
    jieba.suggest_freq('文化生活', True)
    jieba.suggest_freq('家乡的桥', True)
    jieba.suggest_freq('综合实践', True)
    jieba.suggest_freq('社会实践', True)
    jieba.suggest_freq('ie', True)
    jieba.suggest_freq('浏览器', True)
    jieba.suggest_freq('六年级', True)
    jieba.suggest_freq('四年级', True)
    jieba.suggest_freq('清理器', True)
    jieba.suggest_freq('机械设计基础', True)
    jieba.suggest_freq('长媳难为', True)
    jieba.suggest_freq('科学家', True)
    jieba.suggest_freq('地级市', True)
    jieba.suggest_freq('县级市', True)
    jieba.suggest_freq('课前', True)
    jieba.suggest_freq('i5', True)
    jieba.suggest_freq('i7', True)
    jieba.suggest_freq('打印机', True)
    jieba.suggest_freq('手抄报', True)
    jieba.suggest_freq('黑板报', True)
    jieba.suggest_freq('3d', True)
    jieba.suggest_freq('火车票', True)
    jieba.suggest_freq('中国梦', True)
    jieba.suggest_freq('语文园地', True)
    jieba.suggest_freq('久保田', True)
    jieba.suggest_freq('收割机', True)
    jieba.suggest_freq('走光', True)
    jieba.suggest_freq('椿芽', True)
    jieba.suggest_freq('转换器', True)
    jieba.suggest_freq('圆柱形', True)
    jieba.suggest_freq('月考', True)
    jieba.suggest_freq(('安装', '版'), True)
    jieba.suggest_freq(('单元', '测试'), True)
    jieba.suggest_freq(('清明','节'), True)
    jieba.suggest_freq(('申请', '材料'), True)
    jieba.suggest_freq(('最新', '消息'), True)
    jieba.suggest_freq(('公司', '员工'), True)
    jieba.suggest_freq(('规格', '书'), True)
    jieba.suggest_freq(('说明', '书'), True)
    jieba.suggest_freq(('photoshop', 'cc'), True)
    stopword = ['~', '`', '!', '@', '#', '$', '%', '^', '&', '*',
                '(', ')', '_', '-', '+', '=', '[', ']', '{', '}', '\\', '|',
                ';', ':', '\'', '"', ',', '<', '>', '.', '/', '?', ' ', '。', 
                '、', '“', '”', '【', '】', '《', '》']
    english = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
                'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
                'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    connect = [':', '.', '-']
    numbers = list('1234567890')

    data = pd.read_csv(path+'/Data/test_docs.csv')
    token_count = []

    for i, row in tqdm(list(data.iterrows())):
        if str(row['content']) == 'nan' or str(row['doc_title']) == 'nan':
            continue
        else:
            text = row['doc_title'] * title_weight + row['content']
        
        text = list(text)
        for j in range(len(text)):
            if text[j] in english:
                text[j] = text[j].lower()
        j = 1
        while j < len(text):
            if text[j] in stopword:
                try:
                    if text[j] in connect and text[j-1] in numbers and text[j+1] in numbers:
                        pass
                    else:
                        text[j] = ' '
                except: text[j] = ' '
            
            if text[j] in english and text[j-1] not in english:
                text.insert(j, ' ')
                j += 1
            elif text[j-1] in english and text[j] not in english:
                text.insert(j, ' ')
                j += 1
            j += 1

        text = ''.join(text)
    
        tokens = jieba.lcut_for_search(text)

        tokens = [token for token in tokens if token not in stopword]

        tokens = Counter(tokens)
        token_count.append({
            'doc_id': row['doc_id'],
            'doc_url': row['doc_url'],
            'doc_title': row['doc_title'],
            'tokens': tokens
        })

    with open(path+'/Data/docs_token_jieba.json', 'w') as f:
        json.dump(token_count, f, indent=4, ensure_ascii=False)

    spider = json.loads(open(path+'/Data/querys_spider.json').read())
    data = pd.read_csv(path+'/Data/test_querys.csv')
    token_count = {}

    for i, row in tqdm(list(data.iterrows())):
        text = row['query']
        text = list(text)
        if row['query_id'] == 'q23086':   # 清明节黑板报资料
            text.append('手抄报')
        elif row['query_id'] == 'q321561':  # 枪神纪道具城
            text = ['枪神纪道聚城']
        elif row['query_id'] == 'q92794':   # 世界地球日黑板报
            text.append('手抄报')
            text.append(' 世界地球日 世界地球日')
        elif row['query_id'] == 'q56202':
            text.append('由来')
        elif row['query_id'] == 'q365730':
            text.append('鲁滨逊')
        elif row['query_id'] == 'q505758':
            text.append('鲁滨逊')
        elif row['query_id'] == 'q509964':
            text.append('说课稿')
        elif row['query_id'] == 'q121275':
            text.append('申请书')
        elif row['query_id'] == 'q18602':
            text.append('无限火力')
        elif row['query_id'] == 'q184864':
            text.append('一折')
        elif row['query_id'] == 'q59633':
            text.append('申请书')
        elif row['query_id'] == 'q360622':
            text.append('竞选班干部发言稿作文')
        elif row['query_id'] == 'q38184':
            text.append(' ie ie ie ie')
        elif row['query_id'] == 'q365216':
            text.append(' 新颖')
        elif row['query_id'] == 'q95275':
            text.append(' gsm gsm gsm')
        elif row['query_id'] == 'q400532':
            text.append(' 王兆国 王兆国 王兆国')
        elif row['query_id'] == 'q271732':
            text.append(' 隐血 潜血')
        elif row['query_id'] == 'q305643':
            text.append('启示')
        elif row['query_id'] == 'q70519':
            text.append('创业构想规划书')
        elif row['query_id'] == 'q459206':
            text.append('溜冰')
        elif row['query_id'] == 'q203684':
            text.append('翻译')

        for j in range(len(text)):
            if text[j] in english:
                text[j] = text[j].lower()

        j = 1
        while j < len(text):
            if text[j] in stopword and text[j] not in connect:
                text[j] = ' '
            if text[j] in english and text[j-1] not in english:
                text.insert(j, ' ')
                j += 1
            elif text[j-1] in english and text[j] not in english:
                text.insert(j, ' ')
                j += 1
            j += 1

        text = ''.join(text)

        tokens = jieba.lcut_for_search(text)

        tokens = [token for token in tokens if token not in stopword]

        tokens = Counter(tokens)
        token_count[row['query_id']] = {
            'query_id': row['query_id'],
            'query': row['query'],
            'tokens': tokens
        }

    with open(path+'/Data/querys_token_jieba.json', 'w') as f:
        json.dump(token_count, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model','-m', required = True, choices=['pkuseg', 'jieba'])
    parser.add_argument('--weight','-w', type=int)
    args = parser.parse_args()
    if args.weight:
        title_weight = max([0, args.weight])
    else:
        title_weight = 10
    if args.model == 'pkuseg':
        pkuseg_tokenizer(title_weight)
    else:
        jieba_tokenizer(title_weight)
