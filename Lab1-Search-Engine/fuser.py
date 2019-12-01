import pandas as pd
from collections import Counter


# submit1 = pd.read_csv('Lab1-Search-Engine/Data/wzh.csv')
# submit2 = pd.read_csv('Lab1-Search-Engine/Data/submit13-jieba-0.826-0.896.csv')
# submit_fuse = submit1.copy()

# query_ids = submit1['query_id'].unique()

# for n, query_id in enumerate(query_ids):
#     docs1 = submit1[submit1['query_id']==query_id]['doc_id'].tolist()
#     docs2 = submit2[submit2['query_id']==query_id]['doc_id'].tolist()
#     dict1 = {doc:docs1.index(doc) for doc in docs1}
#     dict2 = {doc:docs2.index(doc) for doc in docs2}
#     for key in set(dict1.keys()) | set(dict2.keys()):
#         if key in dict1 and key in dict2:
#             dict1[key] += dict2[key]
#         elif key not in dict1:
#             dict1[key] = dict2[key] + 20
#         else:
#             dict1[key] += 20
#     docs_sort = sorted(dict1.items(), key=lambda d: d[1], reverse=False)
#     docs_sort = [doc[0] for doc in docs_sort]
#     docs = []
#     docs1 = Counter(docs1)
#     docs2 = Counter(docs2)
#     i = 0
#     while len(docs) < 20:
#         if docs2[docs_sort[i]] > 0:
#             docs.append(docs_sort[i])
#             docs2[docs_sort[i]] -= 1
#         else:
#             i += 1
#     submit_fuse.loc[submit_fuse['query_id']==query_id, 'doc_id'] = docs

# submit_fuse.to_csv('Lab1-Search-Engine/Data/submit-fuse.csv', index=False)


submit1 = pd.read_csv('Lab1-Search-Engine/Data/wzh.csv')
submit2 = pd.read_csv('Lab1-Search-Engine/Data/submit13-jieba-0.826-0.896.csv')
submit_fuse = submit1.copy()

query_ids = submit1['query_id'].unique()

for n, query_id in enumerate(query_ids):
    docs1 = submit1[submit1['query_id']==query_id]['doc_id'].tolist()
    docs2 = submit2[submit2['query_id']==query_id]['doc_id'].tolist()
    dict1 = {doc:docs1.index(doc) for doc in docs1}
    dict2 = {doc:docs2.index(doc) for doc in docs2}
    for key in set(dict1.keys()) | set(dict2.keys()):
        if key not in dict1:
            dict1[key] = dict2[key] + 20
    docs_sort = sorted(dict1.items(), key=lambda d: d[1], reverse=False)
    docs_sort = [doc[0] for doc in docs_sort]
    docs = []
    docs1 = Counter(docs1)
    docs2 = Counter(docs2)
    i = 0
    while len(docs) < 20:
        if docs2[docs_sort[i]] > 0:
            docs.append(docs_sort[i])
            docs2[docs_sort[i]] -= 1
        else:
            i += 1
    submit_fuse.loc[submit_fuse['query_id']==query_id, 'doc_id'] = docs

submit_fuse.to_csv('Lab1-Search-Engine/Data/submit-fuse.csv', index=False)