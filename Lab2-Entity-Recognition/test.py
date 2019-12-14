import json
import pandas as pd
import os 


path = os.path.dirname(os.path.abspath(__file__))


def test():
    df = pd.read_csv(path + '/Data/fuse.csv').drop_duplicates()
    answer = json.loads(open(path + '/Data/answer.json').read())

    TP = {'药物': 0, '解剖部位': 0, '疾病和诊断': 0, '手术': 0, '影像检查': 0, '实验室检验': 0}
    TN = {'药物': 0, '解剖部位': 0, '疾病和诊断': 0, '手术': 0, '影像检查': 0, '实验室检验': 0}
    FP = {'药物': 0, '解剖部位': 0, '疾病和诊断': 0, '手术': 0, '影像检查': 0, '实验室检验': 0}
    FN = {'药物': 0, '解剖部位': 0, '疾病和诊断': 0, '手术': 0, '影像检查': 0, '实验室检验': 0}

    for textId in range(600):
        mask = df[df['textId'] == textId]
        labels = mask['label_type'].tolist()
        starts = mask['start_pos'].tolist()
        ends = mask['end_pos'].tolist()
        pre_items = [(labels[i], starts[i], ends[i]) for i in range(len(labels))]
        true_items = [(item['label_type'], item['start_pos'], item['end_pos']) 
                            for item in answer[textId]['entities']]
        for item in pre_items:
            if item in true_items:
                TP[item[0]] += 1
            else:
                FP[item[0]] += 1
        for item in true_items:
            if item not in pre_items:
                FN[item[0]] += 1

    print('\t\tPrecision\tRecall\t\tF1')
    for label in TP.keys():
        precision = TP[label]/(TP[label]+FP[label])
        recall = TP[label]/(TP[label]+FN[label])
        f1 = 2 * precision * recall / (precision + recall)
        print('{:10}\t{:.5f}\t\t{:.5f}\t\t{:.5f}'.format(label, precision, recall, f1))

    TP = sum(TP.values())
    FP = sum(FP.values())
    FN = sum(FN.values())
    precision = TP/(TP+FP)
    recall = TP/(TP+FN)
    f1 = 2 * precision * recall / (precision + recall)
    print('{:10}\t{:.5f}\t\t{:.5f}\t\t{:.5f}'.format('all', precision, recall, f1))


if __name__ == "__main__":
    test()