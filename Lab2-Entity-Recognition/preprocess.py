import json
import os
import pickle
import xmnlp


path = os.path.dirname(os.path.abspath(__file__))

table = {
    '疾病和诊断': 'ILL',
    '药物': 'MDC',
    '手术': 'OPR',
    '解剖部位': 'DSC',
    '影像检查': 'PHT',
    '实验室检验': 'LAB'
}


def read_json(fname):
    fr = open(fname)
    content = fr.read()
    if content.startswith(u'\ufeff'):
            content = content.encode('utf8')[3:].decode('utf8')
    data = []
    lines = content.split('\n')
    for line in lines:
        try: data.append(json.loads(line))
        except: pass
    return data


def process_train(data, fname):
    fr = open(fname, 'w')
    for record in data:
        text = record['originalText']
        entities = record['entities']
        radicals = xmnlp.radical(text)
        i = 0
        j = 0
        while i < len(text):
            if j < len(entities):
                if entities[j]['start_pos'] <= i and i < entities[j]['end_pos']:
                    fr.write('%s\t%s\t%s-%s\n'%(text[i], radicals[i], 'B' if i == entities[j]['start_pos'] else 'I', table[entities[j]['label_type']]))
                    i += 1
                else:
                    fr.write('%s\t%s\t0\n'%(text[i], radicals[i]))
                    if i == entities[j]['end_pos']:
                        j += 1
                    i += 1
            else:
                fr.write('%s\t%s\t0\n'%(text[i], radicals[i]))
                i += 1
        fr.write('\n')


def process_test(data, fname):
    fr = open(fname, 'w')
    for record in data:
        text = record['originalText']
        radicals = xmnlp.radical(text)
        for i in range(len(text)):
            fr.write('%s\t%s\t0\n'%(text[i], radicals[i]))
        fr.write('\n')
    fr.close()


if __name__ == '__main__':
    train_data = read_json(path + '/Data/train.txt')
    process_train(train_data, path + '/Data/train_word.txt')
    test_data = read_json(path + '/Data/test.txt')
    process_test(test_data, path + '/Data/test_word.txt')
