import tensorflow as tf
import numpy as np
import os, argparse, time, random
from model import BiLSTM_CRF
import os

from utils import str2bool, read_corpus, read_dictionary, tag2label, random_embedding, bert_embedding

os.environ['CUDA_VISIBLE_DEVICES']='-1'

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
config.gpu_options.per_process_gpu_memory_fraction = 0.2 

parser = argparse.ArgumentParser()
parser.add_argument('--batch_size', type=int, default=128)
parser.add_argument('--epoch', type=int, default=100)
parser.add_argument('--hidden_dim', type=int, default=300)
parser.add_argument('--optimizer', type=str, default='Adam')
parser.add_argument('--lr', type=float, default=0.001)
parser.add_argument('--clip', type=float, default=5.0)
parser.add_argument('--dropout', type=float, default=0.5)
parser.add_argument('--update_embedding', type=str2bool, default=False)
parser.add_argument('--pretrain_embedding', type=str, default='random')
parser.add_argument('--CRF', type=str2bool, default=True)
parser.add_argument('--embedding_dim', type=int, default=300)
parser.add_argument('--shuffle', type=str2bool, default=True)
parser.add_argument('--train', type=str2bool, default=False)
args = parser.parse_args()


word2id = read_dictionary('word2id.pkl')
# embeddings = random_embedding(word2id, args.embedding_dim)
embeddings = bert_embedding(word2id)
args.embedding_dim = embeddings.shape[1]

predict_path = 'predict.csv' #output
model_path = "saved_model/" + \
    'bs-%d-ep-%d-hd-%d-emb-%d-lr-%.5f/'%(args.batch_size, args.epoch, args.hidden_dim, args.embedding_dim, args.lr)
if not os.path.exists(model_path):
    os.makedirs(model_path)
train_path = 'train_data'
test_path = 'test_data'     #test_data

train_data = read_corpus(train_path)
train_size = len(train_data)
test_data = read_corpus(test_path)
test_size = len(test_data)

if args.train:
    model = BiLSTM_CRF(args, embeddings, tag2label, word2id, output_path=predict_path, model_path=model_path, config=config)
    model.build_graph()
    model.train(train=train_data)
else:
    model_path = tf.train.latest_checkpoint(model_path)
    model = BiLSTM_CRF(args, embeddings, tag2label, word2id, output_path=predict_path, model_path=model_path, config=config)
    model.build_graph()
    labels = model.predict(test_data)
