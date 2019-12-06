import json
import pandas as pd


train = []
for line in open('Lab2-Entity-Recognition/Data/train.txt'):
    item = json.loads(line)
    text = item['originalText']
    entities = item['entities']
    entity_set = set()
    for entity in entities:
        entity_set |= {text[entity['start_pos']:entity['end_pos']]}
    train.append(entity_set)

answer = []
for line in open('Lab2-Entity-Recognition/Data/answer.txt'):
    item = json.loads(line)
    text = item['originalText']
    entities = item['entities']
    entity_set = set()
    for entity in entities:
        input(text[max([0,entity['start_pos']-5]):min([entity['end_pos']+5,len(text)])])
        entity_set |= {text[entity['start_pos']:entity['end_pos']]}
    answer.append(entity_set)

data = []
for i in range(400, 1000):
    # print(i)
    # print(train[i])
    input([a for a in answer[i] if '(' not in a and ')' not in a])




