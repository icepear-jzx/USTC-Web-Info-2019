import surprise 
from surprise import Dataset
from surprise import Reader
from surprise.model_selection import cross_validate
import os
import argparse


path = os.path.dirname(os.path.abspath(__file__))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--model','-m', required = True, 
        choices=['NormalPredictor', 'BaselineOnly', 'KNNBasic', 
                    'KNNWithMeans', 'KNNWithZScore', 'KNNBaseline',
                    'SVD', 'SVDpp', 'NMF', 'SlopeOne', 'CoClustering'])
    args = parser.parse_args()

    file_path = path + '/Data/train_format.txt'
    reader = Reader(line_format='user item rating timestamp', sep=',', rating_scale=(0, 5))
    data = Dataset.load_from_file(file_path, reader=reader)

    if args.model == 'NormalPredictor':
        cross_validate(surprise.NormalPredictor(), data, cv=5, verbose=True)
    elif args.model == 'BaselineOnly':
        cross_validate(surprise.BaselineOnly(), data, cv=5, verbose=True)
    elif args.model == 'KNNBasic':
        cross_validate(surprise.KNNBasic(), data, cv=5, verbose=True)
    elif args.model == 'KNNWithMeans':
        cross_validate(surprise.KNNWithMeans(), data, cv=5, verbose=True)
    elif args.model == 'KNNWithZScore':
        cross_validate(surprise.KNNWithZScore(), data, cv=5, verbose=True)
    elif args.model == 'KNNBaseline':
        cross_validate(surprise.KNNBaseline(), data, cv=5, verbose=True)
    elif args.model == 'SVD':
        cross_validate(surprise.SVD(), data, cv=5, verbose=True)
    elif args.model == 'SVDpp':
        cross_validate(surprise.SVDpp(), data, cv=5, verbose=True)
    elif args.model == 'NMF':
        cross_validate(surprise.NMF(), data, cv=5, verbose=True)
    elif args.model == 'SlopeOne':
        cross_validate(surprise.SlopeOne(), data, cv=5, verbose=True)
    elif args.model == 'CoClustering':
        cross_validate(surprise.CoClustering(), data, cv=5, verbose=True)
