import json
from scipy.sparse import coo_matrix
from scipy.sparse import hstack
import numpy as np
import pickle


class Vectorizer:
	def __init__(self, doc_file='Data/docs_token_pkuseg.json', 
				query_file='Data/querys_token_pkuseg.json'):
		self.doc_file = doc_file
		self.query_file = query_file
		self.docs = json.load(open(self.doc_file))
		self.queries = json.load(open(self.query_file))

		self.word_ind = self.create_word_indices()
		self.vec_len = len(self.word_ind.keys())
		self.df, self.idf = self.calculate_idf()
		self.tf = self.calculate_tf()
		self.tfidf = self.calculate_tfidf()


	def create_word_indices(self, target_file='Data/word_indices.json', load=True):
		if load == True:
			try: return json.load(open(target_file))
			except: pass
		docs = self.docs
		queries = self.queries
		words = {}
		counter = 0
		for doc in docs:
			for word in doc['tokens'].keys():
				if word not in words.keys():
					words[word] = counter
					counter += 1
		for query in queries.values():
			for word in query['tokens'].keys():
				if word not in words.keys():
					words[word] = counter
					counter += 1
		if target_file is not None:
			json.dump(words, open(target_file, 'w'), indent=4, ensure_ascii=False)
		return words


	def doc2vec(self, doc=dict()):
		word_ind = self.word_ind
		vec_len = self.vec_len
		positions = [word_ind[word] for word in doc['tokens'].keys()]
		data = [1 + np.math.log10(num) for num in doc['tokens'].values()]
		return coo_matrix((data, (positions, [0]*len(data))), shape=(vec_len, 1))


	def query2vec(self, query=dict()):
		word_ind = self.word_ind
		vec_len = self.vec_len
		positions = [word_ind[word] for word in query['tokens'].keys()]
		data = [num for num in query['tokens'].values()]
		return coo_matrix((data, (positions, [0]*len(data))), shape=(vec_len, 1))


	def calculate_idf(self, target_file='Data/idf.txt', load=True):
		if load == True:
			try: return None, np.loadtxt(target_file).reshape((-1, 1))
			except: pass
		docs = self.docs
		word_ind = self.word_ind
		num_docs = len(docs)
		df = np.zeros(shape=(self.vec_len), dtype=np.float)
		for doc in docs:
			for word in doc['tokens'].keys():
				df[word_ind[word]] += 1
		df[df == 0] = 1
		idf = np.array([np.math.log10(num_docs/i) for i in df])
		df = df.reshape((-1, 1))
		idf = idf.reshape((-1, 1))
		if target_file is not None:
			np.savetxt(target_file, idf)
		return df, idf


	def calculate_tf(self, target_file='Data/tf.txt', load=True):
		if load == True:
			try: return pickle.load(open(target_file, 'rb'))
			except: pass
		# tf矩阵按照self.docs的文档顺序排列
		docs = self.docs
		tf = []
		for doc in docs:
			tf.append(self.doc2vec(doc))
		tf = hstack(tf)
		pickle.dump(tf, open(target_file, 'wb'))
		return tf

	
	def calculate_tfidf(self, target_file='Data/tfidf.txt', load=True):
		if load == True:
			try: return pickle.load(open(target_file, 'rb'))
			except: pass
		tfidf = self.tf.multiply(self.idf)
		pickle.dump(tfidf, open(target_file, 'wb'))
		return tfidf
