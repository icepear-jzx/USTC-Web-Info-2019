import surprise 
from surprise import Dataset
from surprise import Reader
from surprise.model_selection import cross_validate
import os
import argparse
from tqdm import tqdm


path = os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--model','-m', required = True, 
        choices=['NormalPredictor', 'BaselineOnly', 'KNNBasic', 
                    'KNNWithMeans', 'KNNWithZScore', 'KNNBaseline',
                    'SVD', 'SVDpp', 'NMF', 'SlopeOne', 'CoClustering'])
    args = parser.parse_args()

    train_path = path + '/Data/train_format.txt'
    
    train_reader = Reader(line_format='user item rating timestamp', sep=',', rating_scale=(0, 5))
    trainset = Dataset.load_from_file(train_path, reader=train_reader)
    trainset = trainset.build_full_trainset()

    if args.model == 'NormalPredictor':
        model = surprise.NormalPredictor()
    elif args.model == 'BaselineOnly':
        model = surprise.BaselineOnly()
    elif args.model == 'KNNBasic':
        model = surprise.KNNBasic()
    elif args.model == 'KNNWithMeans':
        model = surprise.KNNWithMeans()
    elif args.model == 'KNNWithZScore':
        model = surprise.KNNWithZScore()
    elif args.model == 'KNNBaseline':
        model = surprise.KNNBaseline()
    elif args.model == 'SVD':
        model = surprise.SVD()
    elif args.model == 'SVDpp':
        model = surprise.SVDpp(verbose=True)
    elif args.model == 'NMF':
        model = surprise.NMF()
    elif args.model == 'SlopeOne':
        model = surprise.SlopeOne()
    elif args.model == 'CoClustering':
        model = surprise.CoClustering()

    # cross_validate(model, trainset, cv=5, verbose=True)
    model.fit(trainset)

    lines = []
    test_path = path + '/Data/test_format.txt'
    for line in tqdm(open(test_path, 'r').readlines()):
        user_id, item_id, timestamp, *tags = line.strip().split(',')
        rating = model.predict(user_id, item_id).est
        lines.append("{:.5}\n".format(float(rating)))
    
    open(path + '/Data/submit.txt', 'w').writelines(lines)

