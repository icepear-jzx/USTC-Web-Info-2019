# Lab1 Search Engine

Given a number of documents and queries, 
return the first 20 most relevant documents for each query.

* Documents are in [test_docs.csv](./Data/test_docs.csv), 
each item has doc_id, doc_url, doc_title and content.
* Queries are in [test_querys.csv](./Data/test_querys.csv), 
each item has query and query_id.
* Submission format is shown in [submission.csv](./Data/submission.csv).

## Installation

You have to be in the root directory of this repository. And then run:

```shell
$ pip3 install -r Lab1-Search-Engine/requirements.txt
```

## Usage

You have to be in the root directory of this repository.

### 1. Segmentation

You can use [pkuseg](https://github.com/lancopku/pkuseg-python) or [jieba](https://github.com/fxsjy/jieba) for segmentation. And set the weight of documents' title by `-m`. The default value is 10.

```shell
$ python3 Lab1-Search-Engine/tokenizer.py -m jieba -w 100
```

### 2. Search

### 3. Sort

### 4. Results

## Explanation


