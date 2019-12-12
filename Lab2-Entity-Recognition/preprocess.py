import json
import os


path = os.path.dirname(os.path.abspath(__file__))

items = []

for line in open(path + '/Data/train.txt').readlines():
    item = json.loads(line)
    items.append(item)

json.dump(items, open(path + '/Data/train.json', 'w'), indent=4, ensure_ascii=False)

# answers = []
# for line in open(path + '/Data/answer.txt').readlines()[400:]:
#     item = json.loads(line)
#     answers.append(item)

# tests = []
# for line in open(path + '/Data/test.txt').readlines():
#     item = json.loads(line)
#     tests.append(item)

# fw = open(path + '/Data/test.json', 'w')
# for i in range(600):
#     answer = answers[i]
#     test = tests[i]
#     test['entities'] = answer['entities']
#     fw.write(json.dumps(test, ensure_ascii=False) + '\n')