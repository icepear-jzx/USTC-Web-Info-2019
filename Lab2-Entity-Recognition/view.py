import pandas as pd 
import json


lines = open('Lab2-Entity-Recognition/Data/test.txt').readlines()
df = pd.read_csv('Lab2-Entity-Recognition/Data/submit.csv')


for i in range(600):
    item = json.loads(lines[i])
    text = item['originalText']
    mask = df[df['textId'] == i]
    labels = mask['label_type'].tolist()
    starts = mask['start_pos'].tolist()
    ends = mask['end_pos'].tolist()
    pre = []
    for j in range(len(labels)):
        pre.append(text[starts[j]:ends[j]])
    input(pre)



