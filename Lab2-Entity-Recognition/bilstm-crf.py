import json



data_answer = []
for line in open('Lab2-Entity-Recognition/Data/answer.txt'):
    item = json.loads(line)
    data_answer.append(item)

i = 0
for line in open('Lab2-Entity-Recognition/Data/test.txt'):
    item = json.loads(line)
    data_answer[400+i]['textId'] = item['textId']
    i += 1

with open('Lab2-Entity-Recognition/Data/answer.json', 'w') as f:
    json.dump(data_answer[400:], f, indent=4, ensure_ascii=False)

