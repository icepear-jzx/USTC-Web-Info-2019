import pkuseg
import pandas as pd
from collections import Counter
import json
from tqdm import tqdm


def pkuseg_tokenizer():
    data = pd.read_csv('Lab1-Search-Engine/Data/test_docs.csv')
    token_count = []

    seg = pkuseg.pkuseg()
    for i, row in tqdm(list(data.iterrows())):
        if str(row['doc_title']) == 'nan' or str(row['content']) == 'nan':
            continue
        else:
            text = seg.cut(row['doc_title'] + row['content'])
        tokens = Counter(text)
        token_count.append({
            'doc_id': row['doc_id'], 
            'doc_url': row['doc_url'], 
            'doc_title': row['doc_title'],
            'tokens': tokens
        })

    with open('Lab1-Search-Engine/Data/docs_token_pkuseg.json', 'w') as f:
        json.dump(token_count, f, indent=4, ensure_ascii=False)

    data = pd.read_csv('Lab1-Search-Engine/Data/test_querys.csv')
    token_count = []

    seg = pkuseg.pkuseg()
    for i, row in tqdm(list(data.iterrows())):
        text = seg.cut(row['query'])
        tokens = Counter(text)
        token_count.append({
            'query_id': row['query_id'],
            'query': row['query'],
            'tokens': tokens
        })

    with open('Lab1-Search-Engine/Data/querys_token_pkuseg.json', 'w') as f:
        json.dump(token_count, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    pkuseg_tokenizer()
