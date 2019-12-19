# Lab1 Search Engine

Given a number of documents and queries, 
return the first 20 most relevant documents for each query.

* Documents are in [test_docs.csv](./Data/test_docs.csv), 
each item has `doc_id`, `doc_url`, `doc_title` and `content`.
* Queries are in [test_querys.csv](./Data/test_querys.csv), 
each item has `query` and `query_id`.
* Submission format is shown in [submission.csv](./Data/submission.csv).

More details: [http://staff.ustc.edu.cn/~tongxu/webinfo/slides/exp1.pdf](http://staff.ustc.edu.cn/~tongxu/webinfo/slides/exp1.pdf)

## Installation

```shell
$ pip3 install -r requirements.txt --user
```

## Usage

You have to be in the root directory of this repository.

### 1. Segmentation

You can use [pkuseg](https://github.com/lancopku/pkuseg-python) or [jieba](https://github.com/fxsjy/jieba) for segmentation. And set the weight of document title by `-w`. The default value is 10.

```shell
$ python3 tokenizer.py -m jieba -w 100
```

The output files are `docs_token_jieba.json` and `querys_token_jieba.json` in `Data/`.

### 2. Search

Calculate tf-idf and select top 20 documents for each query.

```shell
$ python3 searcher.py
```

You will get `submit.csv` as a preliminary result and other intermediate files.

### 3. Reorder

Setting the weight of title can improve recall score but F1 score might decline. To improve F1 score, you'd better reorder the top 20 documents for each query.

```shell
$ python3 tokenizer.py -m jieba -w 1
$ python3 sorter.py 
```

### 4. Results

The final result is `submit-sorted.csv`.

You can see my results and scores in `Data/`.

## Explanation

My report: [report-lab1.pdf](./report-lab1.pdf).
