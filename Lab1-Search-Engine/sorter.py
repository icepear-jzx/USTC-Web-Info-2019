import json
from scipy.sparse import coo_matrix
from scipy import matrix
from scipy.sparse import hstack
import numpy as np
from vectorizer import Vectorizer
import pandas as pd
from tqdm import tqdm


class Searcher(Vectorizer):
	def __init__(self, doc_file='Lab1-Search-Engine/Data/docs_token_jieba.json', 
				query_file='Lab1-Search-Engine/Data/querys_token_jieba.json'):
		super().__init__(doc_file=doc_file, query_file=query_file)
		self.source_file = pd.read_csv('Lab1-Search-Engine/Data/submit-fuse.csv')
		

	# simmode: 0 for inner product, 1 for cosine, 2 for pearson
	def search(self, qid, simmode=0):
		docs_unsorted = self.source_file[self.source_file['query_id']==qid]['doc_id'].tolist()
		qvec = self.query2vec(self.queries[qid])
		if simmode == 0:
			sim = np.array(self.tfidf.multiply(qvec).sum(axis=0)).reshape((-1))
		elif simmode == 1:
			doc_norm = np.sqrt((self.tfidf.power(2)).sum(axis=0))
			query_norm = float(np.sqrt((qvec.power(2)).sum()))
			sim = np.array(self.tfidf.multiply(qvec).sum(axis=0)/(doc_norm*query_norm)).reshape((-1))
		idx = np.where(sim > 0)[0]
		sim = sim[idx]
		idxx = np.argsort(-sim)
		idx_sorted = []
		for i in idx[idxx]:
			if self.docs[i]['doc_id'] in docs_unsorted:
				idx_sorted.append(i)
			if len(idx_sorted) == 20:
				break
		while len(idx_sorted) < 20:
			idx_sorted.append(idx[idxx][0])
		return [self.docs[i]['doc_id'] for i in idx_sorted], [self.docs[i]['doc_title'] for i in idx_sorted]

	
	def create_submission(self, org_file='Lab1-Search-Engine/Data/submission.csv', 
			target_file='Lab1-Search-Engine/Data/submit.csv'):
		question = pd.read_csv(org_file)
		qids = question['query_id']
		dids = []
		for qid in tqdm(list(qids.unique())):
			results, _ = self.search(qid)
			dids += results
		answer = pd.DataFrame()
		answer['query_id'] = qids
		answer['doc_id'] = dids
		answer.to_csv(target_file, index=False)


if __name__ == '__main__':
	Searcher().create_submission()
