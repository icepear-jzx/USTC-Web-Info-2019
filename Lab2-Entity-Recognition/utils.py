import pickle
import os
import numpy as np
import random
import argparse
import pandas as pd


tag2label = {"0": 0,
             "B-ILL": 1, "I-ILL": 2,
             "B-MDC": 3, "I-MDC": 4,
             "B-OPR": 5, "I-OPR": 6,
             "B-DSC": 7, "I-DSC": 8,
             "B-PHT": 9, "I-PHT": 10,
             "B-LAB": 11, "I-LAB": 12,
             }


word2label = {
    '疾病和诊断': 'ILL',
    '药物': 'MDC',
    '手术': 'OPR',
    '解剖部位': 'DSC',
    '影像检查': 'PHT',
    '实验室检验': 'LAB'
}


def read_dictionary(vocab_path):
    vocab_path = os.path.join(vocab_path)
    with open(vocab_path, 'rb') as fr:
        word2id = pickle.load(fr)
    print('vocab_size:', len(word2id))
    return word2id


def read_corpus(corpus_path):
    data = []
    with open(corpus_path, encoding='utf-8') as fr:
        lines = fr.readlines()
    sent_, tag_ = [], []
    for line in lines:
        if line != '\n':
            stripped = line.strip().split()
            if len(stripped) == 2:
                [char, label] = stripped
                sent_.append(char)
                tag_.append(label)
        else:
            data.append((sent_, tag_))
            sent_, tag_ = [], []

    return data


def vocab_build(vocab_path, corpus_path, min_count):
    data = read_corpus(corpus_path)
    word2id = {}
    for sent_, tag_ in data:
        for word in sent_:
            if word.isdigit():
                word = '<NUM>'
            elif ('\u0041' <= word <='\u005a') or ('\u0061' <= word <='\u007a'):
                word = '<ENG>'
            if word not in word2id:
                word2id[word] = [len(word2id)+1, 1]
            else:
                word2id[word][1] += 1
    low_freq_words = []
    for word, [word_id, word_freq] in word2id.items():
        if word_freq < min_count and word != '<NUM>' and word != '<ENG>':
            low_freq_words.append(word)
    for word in low_freq_words:
        del word2id[word]

    new_id = 1
    for word in word2id.keys():
        word2id[word] = new_id
        new_id += 1
    word2id['<UNK>'] = new_id
    word2id['<PAD>'] = 0

    with open(vocab_path, 'wb') as fw:
        pickle.dump(word2id, fw)

    
def random_embedding(vocab, embedding_dim):
    embedding_mat = np.random.uniform(-0.25, 0.25, (len(vocab), embedding_dim))
    embedding_mat = np.float32(embedding_mat)
    return embedding_mat


def pad_sequences(sequences, pad_mark=0):
    max_len = max(map(lambda x : len(x), sequences))
    seq_list, seq_len_list = [], []
    for seq in sequences:
        seq = list(seq)
        seq_ = seq[:max_len] + [pad_mark] * max(max_len - len(seq), 0)
        seq_list.append(seq_)
        seq_len_list.append(min(len(seq), max_len))
    return seq_list, seq_len_list



def sentence2id(sent, word2id):
    sentence_id = []
    for word in sent:
        if word.isdigit():
            word = '<NUM>'
        elif ('\u0041' <= word <= '\u005a') or ('\u0061' <= word <= '\u007a'):
            word = '<ENG>'
        if word not in word2id:
            word = '<UNK>'
        sentence_id.append(word2id[word])
    return sentence_id



def batch_yield(data, batch_size, vocab, tag2label, shuffle=False):
    if shuffle:
        random.shuffle(data)

    seqs, labels = [], []
    for (sent_, tag_) in data:
        sent_ = sentence2id(sent_, vocab)
        label_ = [tag2label[tag] for tag in tag_]

        if len(seqs) == batch_size:
            yield seqs, labels
            seqs, labels = [], []

        seqs.append(sent_)
        labels.append(label_)

    if len(seqs) != 0:
        yield seqs, labels


def make_df(data, labels):
    result = pd.DataFrame(columns=['textId','label_type','start_pos','end_pos'])
    for i in range(len(data)):
        cur_label = '0'
        start_pos = 0
        for j in range(len(labels[i])):
            label = list(tag2label.keys())[list(tag2label.values()).index(labels[i][j])]
            if label[0] == 'B':
                if cur_label != '0':
                    word = list(word2label.keys())[list(word2label.values()).index(cur_label)]
                    result = result.append([{'textId': i, 'label_type':word, 'start_pos': start_pos, 'end_pos': j}])
                start_pos = j
                cur_label = label[2:]

            elif label[0] == '0':
                if cur_label != '0':
                    word = list(word2label.keys())[list(word2label.values()).index(cur_label)]
                    result = result.append([{'textId': i, 'label_type':word, 'start_pos': start_pos, 'end_pos': j}])
                cur_label = '0'
    return result


def str2bool(v):
    # copy from StackOverflow
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')