import pandas as pd


def compare():
    docs = pd.read_csv('Lab1-Search-Engine/Data/test_docs.csv')
    querys = pd.read_csv('Lab1-Search-Engine/Data/test_querys.csv')

    submit1 = pd.read_csv('Lab1-Search-Engine/Data/submit7-jieba-0.812-0.883.csv')
    submit2 = pd.read_csv('Lab1-Search-Engine/Data/submit.csv')
    # submit_fuse = submit1.copy()

    query_ids = submit1['query_id'].unique()

    for n, query_id in enumerate(query_ids):
        print(n, querys[querys['query_id']==query_id]['query'].values[0])
        docs1 = submit1[submit1['query_id']==query_id]['doc_id'].tolist()
        docs2 = submit2[submit2['query_id']==query_id]['doc_id'].tolist()
        # docs1_diff = []
        # docs2_diff = []
        for doc in docs1:
            if doc not in docs2:
                # docs1_diff.append(doc)
                print('submit1:', doc, docs[docs['doc_id']==doc]['doc_title'])
        for doc in docs2:
            if doc not in docs1:
                # docs2_diff.append(doc)
                print('submit2:', doc, docs[docs['doc_id']==doc]['doc_title'])
        choice = input()
        # if choice == '2':
        #     submit_fuse[submit_fuse['query_id']==query_id] = submit2[submit2['query_id']==query_id]


def view():
    docs = pd.read_csv('Lab1-Search-Engine/Data/test_docs.csv')
    querys = pd.read_csv('Lab1-Search-Engine/Data/test_querys.csv')
    submit1 = pd.read_csv('Lab1-Search-Engine/Data/submit.csv')

    query_ids = submit1['query_id'].unique()

    for n, query_id in enumerate(query_ids):
        print(n, querys[querys['query_id']==query_id]['query'].values[0])
        docs1 = submit1[submit1['query_id']==query_id]['doc_id'].tolist()
        for doc in docs1:
            print(doc, docs[docs['doc_id']==doc]['doc_title'].values)
            # print(docs[docs['doc_id']==doc]['content'].values[0])
        input()


compare()
