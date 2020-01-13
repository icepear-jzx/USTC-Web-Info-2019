import pickle
import os
from tqdm import tqdm
import time


path = os.path.dirname(os.path.abspath(__file__))


def id2index():
    user_ids = set()
    item_ids = set()

    for line in tqdm(open(path + '/Data/train.txt', 'r').readlines()):
        user_id, item_id, rating, time, *tags = line.strip().split(',')
        user_ids |= set([user_id])
        item_ids |= set([item_id])

    for line in tqdm(open(path + '/Data/test.txt', 'r').readlines()):
        user_id, item_id, time = line.strip().split(',')[:3]
        user_ids |= set([user_id])
        item_ids |= set([item_id])
    
    for line in tqdm(open(path + '/Data/contacts.txt', 'r').readlines()):
        user, contacts = line.strip().split(':')
        contacts = contacts.split(',')
        user_ids |= set([user])
        for contact in contacts: 
            user_ids |= set([contact])
    
    user_ids = list(user_ids)
    item_ids = list(item_ids)
    userid2index = {user_ids[i]: i for i in range(len(user_ids))}
    itemid2index = {item_ids[i]: i for i in range(len(item_ids))}
    pickle.dump(userid2index, open(path + '/Data/userid2index.pkl', 'wb'))
    pickle.dump(itemid2index, open(path + '/Data/itemid2index.pkl', 'wb'))


def format_trainset():
    # userid2index = pickle.load(open(path + '/Data/userid2index.pkl', 'rb'))
    # itemid2index = pickle.load(open(path + '/Data/itemid2index.pkl', 'rb'))
    lines = []

    for line in tqdm(open(path + '/Data/train.txt', 'r').readlines()):
        user_id, item_id, rating, date, *tags = line.strip().split(',')
        timestamp = time.mktime(time.strptime(date[:19], "%Y-%m-%dT%H:%M:%S"))
        lines.append("{},{},{},{}\n".format(user_id, item_id, rating, timestamp))
    
    open(path + '/Data/train_format.txt', 'w').writelines(lines)


def format_testset():
    # userid2index = pickle.load(open(path + '/Data/userid2index.pkl', 'rb'))
    # itemid2index = pickle.load(open(path + '/Data/itemid2index.pkl', 'rb'))
    lines = []

    for line in tqdm(open(path + '/Data/test.txt', 'r').readlines()):
        user_id, item_id, date, *tags = line.strip().split(',')
        timestamp = time.mktime(time.strptime(date[:19], "%Y-%m-%dT%H:%M:%S"))
        lines.append("{},{},{}\n".format(user_id, item_id, timestamp))
    
    open(path + '/Data/test_format.txt', 'w').writelines(lines)


def format_contacts():
    userid2index = pickle.load(open(path + '/Data/userid2index.pkl', 'rb'))
    lines = []

    for line in tqdm(open(path + '/Data/contacts.txt', 'r').readlines()):
        user, contacts = line.strip().split(':')
        contacts = contacts.split(',')
        for contact in contacts: 
            lines.append("{},{},1\n".format(userid2index[user], userid2index[contact]))
    
    open(path + '/Data/contacts_format.txt', 'w').writelines(lines)


if __name__ == "__main__":
    # id2index()
    format_trainset()
    format_testset()
    # format_contacts()

    user_ids = set()
    for line in tqdm(open(path + '/Data/test.txt', 'r').readlines()):
        user_id, item_id, time = line.strip().split(',')[:3]
        user_ids |= set([user_id])
    user_ids = list(user_ids)
    pickle.dump(user_ids, open(path + '/Data/userlist.pkl', 'wb'))
