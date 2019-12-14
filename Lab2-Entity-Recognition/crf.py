import sklearn_crfsuite
import os
from tqdm import tqdm
import sys
import pandas as pd
import test


path = os.path.dirname(os.path.abspath(__file__))


def word2features(sent, i):
    punctuations = [' ', '+', '，', '-', '：', '、', '.', '；', '。', '？',
        '/', '*', '\\', '(', ')', '（', '）', '”', '“', '"']
    word = sent[i][0]
    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        # 'word.isdigit()': word.isdigit(),
        # 'word.ispunc()': word in punctuations
    }

    if i > 0:
        word1 = sent[i-1][0]
        features.update({
            '-1:word.lower()': word1.lower(),
            # '-1:word.isdigit()': word1.isdigit(),
            # '-1:word.ispunc()': word1 in punctuations,
            '-1+0:words.lower()': word1.lower() + word.lower()
        })
    else:
        features['BOS'] = True

    if i < len(sent)-1:
        word1 = sent[i+1][0]
        features.update({
            '+1:word.lower()': word1.lower(),
            # '+1:word.isdigit()': word1.isdigit(),
            # '+1:word.ispunc()': word1 in punctuations,
            '0+1:words.lower()': word.lower() + word1.lower()
        })
    else:
        features['EOS'] = True

    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]


def sent2labels(sent):
    return [label for token, label in sent]


def sent2tokens(sent):
    return [token for token, label in sent]


def labels2csv(pred):
    tag2label = {
        'ILL': '疾病和诊断',
        'MDC': '药物',
        'OPR': '手术',
        'DSC': '解剖部位',
        'PHT': '影像检查',
        'LAB': '实验室检验'
    }
    submit = {'textId':[], 'label_type':[], 'start_pos':[], 'end_pos':[]}
    for i in range(len(pred)):
        start_pos = 0
        end_pos = 0
        for j in range(len(pred[i])):
            tag = pred[i][j]

            if tag[0] == 'B':
                start_pos = j
            
            if tag != '0' and (j == len(pred[i])-1 or pred[i][j+1][0] != 'I'):
                end_pos = j + 1
                if start_pos < end_pos:
                    submit['textId'].append(i)
                    submit['label_type'].append(tag2label[tag[-3:]])
                    submit['start_pos'].append(start_pos)
                    submit['end_pos'].append(end_pos)
    
    submit = pd.DataFrame(submit).drop_duplicates()
    submit.to_csv(path + '/Data/submit.csv', index=False)


if __name__ == "__main__":

    train_sents = []
    sent = []
    for line in open(path + '/Data/train_word.txt'):
        s = line[:-1].split('\t')
        if len(s) == 2:
            sent.append((s[0], s[1]))
        else:
            train_sents.append(sent)
            sent = []
        
    test_sents = []
    sent = []
    for line in open(path + '/Data/test_word.txt'):
        s = line[:-1].split('\t')
        if len(s) == 2:
            sent.append((s[0], s[1]))
        else:
            test_sents.append(sent)
            sent = []
    
    x_train = [sent2features(s) for s in tqdm(train_sents)]

    y_train = [sent2labels(s) for s in tqdm(train_sents)]

    x_test = [sent2features(s) for s in tqdm(test_sents)]

    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.2,
        c2=0.1,
        max_iterations=100,
        all_possible_transitions=True,
        all_possible_states=True,
        verbose=True
    )

    crf.fit(x_train, y_train)

    y_pred = crf.predict(x_test)

    labels2csv(y_pred)
