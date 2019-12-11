import os
import json
import pandas as pd



path = os.path.dirname(os.path.abspath(__file__))

rule = pd.read_csv(path + '/Data/rule.csv')
submit = pd.read_csv(path + '/Data/submit1-0.6296.csv')
fuse = {'textId':[], 'label_type':[], 'start_pos':[], 'end_pos':[]}

for textId in range(600):
    rule_sub = rule[rule['textId'] == textId]
    rule_labels = rule_sub['label_type'].tolist()
    rule_starts = rule_sub['start_pos'].tolist()
    rule_ends = rule_sub['end_pos'].tolist()
    submit_sub = submit[submit['textId'] == textId]
    submit_labels = submit_sub['label_type'].tolist()
    submit_starts = submit_sub['start_pos'].tolist()
    submit_ends = submit_sub['end_pos'].tolist()
    for i in range(len(submit_labels)):
        label_type = submit_labels[i]
        start_pos = submit_starts[i]
        end_pos = submit_ends[i]
        # if label_type == '药物':
        #     continue
        for j in range(len(rule_labels)):
            if start_pos < rule_ends[j] and end_pos > rule_starts[j]:
                break
        else:
            fuse['textId'].append(textId)
            fuse['label_type'].append(label_type)
            fuse['start_pos'].append(start_pos)
            fuse['end_pos'].append(end_pos)
    for i in range(len(rule_labels)):
        fuse['textId'].append(textId)
        fuse['label_type'].append(rule_labels[i])
        fuse['start_pos'].append(rule_starts[i])
        fuse['end_pos'].append(rule_ends[i])

fuse = pd.DataFrame(fuse).drop_duplicates()
fuse.to_csv(path + '/Data/fuse.csv', index=False)


