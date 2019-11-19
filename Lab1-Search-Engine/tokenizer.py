import pkuseg
import pandas as pd
from collections import Counter
import json
from tqdm import tqdm


def pkuseg_tokenizer():
    seg = pkuseg.pkuseg(postag=True)
    stopword_tags = []
    # stopword_tags = ['m', 'q', 'r', 'd', 'p', 'c', 'u', 'y', 'e', 'o', 'w']
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

    # data = pd.read_csv('Lab1-Search-Engine/Data/test_docs.csv')
    # token_count = []

    # for i, row in tqdm(list(data.iterrows())):
    #     if str(row['content']) == 'nan' and str(row['doc_title']) == 'nan':
    #         continue
    #     elif str(row['content']) == 'nan':
    #         text = row['doc_title']
    #     elif str(row['doc_title']) == 'nan':
    #         text = row['content']
    #     else:
    #         text = row['doc_title'] * 10 + row['content']
        
    #     text = list(text)
    #     for j in range(len(text)):
    #         if text[j] in english:
    #             text[j] = text[j].lower()
    #     j = 1
    #     while j < len(text):
    #         if text[j] in stopword:
    #             try:
    #                 if text[j] in connect and text[j-1] in numbers and text[j+1] in numbers:
    #                     pass
    #                 else:
    #                     text[j] = ' '
    #             except: text[j] = ' '
            
    #         if text[j] in english and text[j-1] not in english:
    #             text.insert(j, ' ')
    #             j += 1
    #         elif text[j-1] in english and text[j] not in english:
    #             text.insert(j, ' ')
    #             j += 1
    #         j += 1

    #     text = ''.join(text)

    #     tokens = seg.cut(text)

    #     tokens = [token for token, tag in tokens 
    #         if tag not in stopword_tags and token not in stopword]

    #     tokens = Counter(tokens)
    #     token_count.append({
    #         'doc_id': row['doc_id'],
    #         'doc_url': row['doc_url'],
    #         'doc_title': row['doc_title'],
    #         'tokens': tokens
    #     })

    # with open('Lab1-Search-Engine/Data/docs_token_pkuseg.json', 'w') as f:
    #     json.dump(token_count, f, indent=4, ensure_ascii=False)

    data = pd.read_csv('Lab1-Search-Engine/Data/test_querys.csv')
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

    with open('Lab1-Search-Engine/Data/querys_token_pkuseg.json', 'w') as f:
        json.dump(token_count, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    pkuseg_tokenizer()
