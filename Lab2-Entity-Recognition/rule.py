import os
import re
import json
import pandas as pd
from tqdm import tqdm

path = os.path.dirname(os.path.abspath(__file__))


def get_rules(path):
    return [rule.strip() for rule in open(path).readlines()]
    

def get_answers(path):
    answers = []
    for line in open(path):
        item = json.loads(line)
        item['entities'] = [(entity['label_type'], entity['start_pos'], entity['end_pos']) 
                            for entity in item['entities']]
        answers.append(item)
    return answers


def get_tests(path):
    tests = []
    for line in open(path):
        item = json.loads(line)
        tests.append(item)
    return tests


def get_trains(path):
    trains = []
    for line in open(path):
        item = json.loads(line)
        item['entities'] = [(entity['label_type'], entity['start_pos'], entity['end_pos']) 
                            for entity in item['entities']]
        trains.append(item)
    return trains


def norule_transfer(s):
    transfer = {'+': '\\+', '(': '\\(', ')': '\\)'}
    for key, value in transfer.items():
        s = s.replace(key, value)
    return s


def rule_match(rule, item):
    match_items = []
    match_list = list(re.finditer(rule, item['originalText']))
    for match_obj in match_list:
        label, name = list(match_obj.groupdict().items())[0]
        span = match_obj.span()
        len_name = len(name)
        name = norule_transfer(name)
        try:
            offset = re.search(name, item['originalText'][span[0]:span[1]]).start()
        except AttributeError:
            print(name)
        tmp_obj = (label, span[0]+offset, span[0]+offset+len_name)
        match_items.append(tmp_obj)
    return match_items


def test_rule(rule, answers):
    TP = 0
    FP = 0
    for answer in answers:
        match_items = rule_match(rule, answer)
        for item in match_items:
            if item in answer['entities']:
                TP += 1
            else:
                FP += 1
    return TP, FP


def view_omitted(rules, answer):
    for answer in answers:
        entities_omitted = answer['entities']
        for rule in rules:
            match_items = rule_match(rule, answer)
            for entity in match_items:
                if entity in entities_omitted:
                    entities_omitted.remove(entity)
        text = answer['originalText']
        for entity in entities_omitted:
            if entity[2] - entity[1] < 10:
                print(text[max((entity[1]-5,0)):min((entity[2]+5,len(text)))], 
                        '\t\t', text[entity[1]:entity[2]], '\t\t', entity[0])
        input()


def gen_rules(trains, answers, path):
    rules = []
    for item in tqdm(trains):
        text = item['originalText']
        for entity in item['entities']:
            if entity[0] == '药物':
                name = norule_transfer(text[entity[1]:entity[2]])
                rule = '(?P<药物>{})'.format(name)
            elif entity[0] == '手术':
                name = norule_transfer(text[entity[1]:entity[2]])
                rule = '(?P<手术>{})'.format(name)
            elif entity[0] == '解剖部位':
                name = norule_transfer(text[entity[1]:entity[2]])
                rule = '(?P<解剖部位>{})'.format(name)
            elif entity[0] == '疾病和诊断':
                name = norule_transfer(text[entity[1]:entity[2]])
                rule = '(?P<疾病和诊断>{})'.format(name)
            elif entity[0] == '影像检查':
                name = norule_transfer(text[entity[1]:entity[2]])
                rule = '(?P<影像检查>{})'.format(name)
            elif entity[0] == '实验室检验':
                name = norule_transfer(text[entity[1]:entity[2]])
                rule = '(?P<实验室检验>{})'.format(name)
            TP, FP = test_rule(rule, answers)
            precision = TP / (TP + FP + 0.000001)
            if precision > 0.9:
                rules.append(rule + '\r\n')
    rules = list(set(rules))
    with open(path, 'w') as fw:
        fw.writelines(rules)
    

def gen_submit(rules, tests, path):
    submit = {'textId':[], 'label_type':[], 'start_pos':[], 'end_pos':[]}
    for test in tqdm(tests):
        for rule in rules:
            match_items = rule_match(rule, test)
            for item in match_items:
                submit['textId'].append(tests.index(test))
                submit['label_type'].append(item[0])
                submit['start_pos'].append(item[1])
                submit['end_pos'].append(item[2])
    submit = pd.DataFrame(submit).drop_duplicates()
    submit.to_csv(path, index=False)


if __name__ == "__main__":

    answers = get_answers(path + '/Data/answer.txt')

    tests = get_tests(path + '/Data/test.txt')

    trains = get_trains(path + '/Data/train.txt')

    gen_rules(trains, trains, path + '/Data/auto-rules.txt')
    
    manual_rules = get_rules(path + '/Data/manual-rules.txt')

    auto_rules = get_rules(path + '/Data/auto-rules.txt')

    rules = auto_rules + manual_rules

    gen_submit(rules, tests, path + '/Data/rule.csv')

    # for rule in manual_rules:
    #     TP, FP = test_rule(rule, answers)
    #     print('Rule:', rule, '\t\tTP:', TP, '\t\tFP:', FP, '\t\tPrecision:', TP / (TP + FP))
    
    # view_omitted(rules, answers)

