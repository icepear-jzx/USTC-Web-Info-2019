import json
from scipy.sparse import coo_matrix
from scipy.sparse import hstack
import numpy as np
from vectorizer import Vectorizer
import pandas as pd
from tqdm import tqdm


class Searcher(Vectorizer):
	def __init__(self, doc_file='Lab1-Search-Engine/Data/docs_token_pkuseg.json', 
				query_file='Lab1-Search-Engine/Data/querys_token_pkuseg.json'):
		super().__init__(doc_file=doc_file, query_file=query_file)
		
	
	def search(self, qid):
		qvec = self.query2vec(self.queries[qid])
		sim = np.array(self.tfidf.multiply(qvec).sum(axis=0)).reshape((-1))
		idx = np.where(sim > 0)[0]
		sim = sim[idx]
		idxx = np.argsort(-sim)
		idx = list(idx[idxx])
		while len(idx) < 20:
			rand = np.random.randint(0, self.tfidf.shape[1])
			if rand not in idx:
				idx.append(rand)
		return [self.docs[i]['doc_id'] for i in idx[:20]], [self.docs[i]['doc_title'] for i in idx[:20]]

	
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
	