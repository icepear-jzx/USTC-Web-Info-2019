import json
import pandas as pd


df = pd.read_csv('Lab2-Entity-Recognition/Data/submit.csv').drop_duplicates()
answer = json.loads(open('Lab2-Entity-Recognition/Data/answer.json').read())

TP = 0
TN = 0
FP = 0
FN = 0

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
            TP += 1
        else:
            FP += 1
    for item in true_items:
        if item not in pre_items:
            FN += 1

precision = TP/(TP+FP)
recall = TP/(TP+FN)
f1 = 2 * precision * recall / (precision + recall)
print('Precision:', precision)
print('Recall:', recall)
print('F1:', f1)
