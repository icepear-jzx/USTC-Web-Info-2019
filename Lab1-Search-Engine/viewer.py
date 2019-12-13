import pandas as pd
import os


path = os.path.dirname(os.path.abspath(__file__))


def compare():
    docs = pd.read_csv(path+'/Data/test_docs.csv')
    querys = pd.read_csv(path+'/Data/test_querys.csv')

    submit1 = pd.read_csv(path+'/Data/submit-fuse.csv')
    submit2 = pd.read_csv(path+'/Data/submit13-jieba-0.826-0.896.csv')
    submit_fuse = submit1.copy()

    query_ids = submit1['query_id'].unique()

    for n, query_id in enumerate(query_ids):
        print(n, querys[querys['query_id']==query_id]['query'].values[0])
        docs1 = submit1[submit1['query_id']==query_id]['doc_id'].tolist()
        docs2 = submit2[submit2['query_id']==query_id]['doc_id'].tolist()
        # docs1_diff = []
        # docs2_diff = []
        # for i in range(20):
        #     print(docs1[i], docs2[i])
        for doc in docs1:
            if doc not in docs2:
                # docs1_diff.append(doc)
                print('submit1:', doc, docs[docs['doc_id']==doc]['doc_title'])
        for doc in docs2:
            if doc not in docs1:
                # docs2_diff.append(doc)
                print('submit2:', doc, docs[docs['doc_id']==doc]['doc_title'])
        choice = input()
        if choice == '2':
            submit_fuse[submit_fuse['query_id']==query_id] = submit2[submit2['query_id']==query_id]
    
    submit_fuse.to_csv(path+'/Data/submit-fuse.csv', index=False)


def view():
    docs = pd.read_csv(path+'/Data/test_docs.csv')
    querys = pd.read_csv(path+'/Data/test_querys.csv')
    submit1 = pd.read_csv(path+'/Data/submit10-jieba-0.825-0.889.csv')

    query_ids = submit1['query_id'].unique()

    for n, query_id in enumerate(query_ids):
        print(n, querys[querys['query_id']==query_id]['query'].values[0])
        docs1 = submit1[submit1['query_id']==query_id]['doc_id'].tolist()
        for doc in docs1:
            print(doc, docs[docs['doc_id']==doc]['doc_title'].values)
        input()


if __name__ == "__main__":
    # view()
    compare()
