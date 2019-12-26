import os, json
from tqdm import tqdm


path = os.path.dirname(os.path.abspath(__file__))



def test():

    userlist_got = [filename[:-5] for filename in os.listdir(path + '/Data/Movie')]

    lines = []

    userlist_wrong = set()

    now_user = '0'
    now_movies = {}
    now_all = 0
    now_right = 0
    all_all = 0
    all_right = 0
    for line in tqdm(open(path + '/Data/train.txt', 'r').readlines()[:7089960]):
        user_id, item_id, rating, time, *tags = line.strip().split(',')
        if user_id != now_user:
            if user_id in userlist_got:
                if now_all != 0:
                    print(now_user, now_right / now_all)
                now_movies = json.load(open(path + '/Data/Movie/{}.json'.format(user_id)))
                now_user = user_id
                now_all = 0
                now_right = 0
            else:
                lines.append('NaN\n')
                continue
        
        if item_id in now_movies:
            spider_rating = now_movies[item_id]['rating']
            lines.append('{}\n'.format(spider_rating))
        else:
            lines.append('NaN\n')
            continue
        
        now_all += 1
        all_all += 1
        if spider_rating != rating:
            # print('Wrong:', spider_rating, rating, user_id, item_id, time)
            userlist_wrong |= set([now_user])
        else:
            now_right += 1
            all_right += 1
        # else:
        #     print('Right!')
    # print(userlist_wrong)
    print(len(userlist_wrong), len(userlist_got))
    print(all_right / all_all)


def fuse():

    userlist_got = [filename[:-5] for filename in os.listdir(path + '/Data/Movie')]

    rating_lines = open(path + '/Data/svd-0.9499-1.3412.txt').readlines()

    test_lines = open(path + '/Data/test.txt', 'r').readlines()

    now_user = '0'
    now_movies = {}
    
    for i in tqdm(range(len(test_lines))):
        user_id, item_id, time, *tags = test_lines[i].strip().split(',')
        if user_id != now_user:
            if user_id in userlist_got:
                now_movies = json.load(open(path + '/Data/Movie/{}.json'.format(user_id)))
                now_user = user_id
            else:
                continue
        
        if item_id in now_movies:
            rating_lines[i] = now_movies[item_id]['rating'] + '\n'

    open(path + '/Data/fuse.txt', 'w').writelines(rating_lines)


fuse()
# test()
