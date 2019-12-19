# USTC-Web-Info

> Labs of 2019 Web Information Processing and Application in USTC.

## Download

```shell
$ git clone https://github.com/IcePear-Jzx/USTC-Web-Info.git --depth 1
```

> Notice: Only part of data is remianed. You need to find and download complete data by yourself.

## Lab0 Web Spider

[Douban](https://www.douban.com) is a community website where users give comments about books, movies, music and so on. 
The goal of this lab is to use web spider to get books' information from [Douban Books](https://book.douban.com).

* Get the top 250 book's information.
* Get all books' URLs.
* Design distributed technique or parallel technique.

More details:
[https://git.bdaa.pro/yxonic/data-specification/wikis/豆瓣%20书评](https://git.bdaa.pro/yxonic/data-specification/wikis/豆瓣%20书评)

## Lab1 Search Engine

Given a number of documents and queries, 
return the first 20 most relevant documents for each query.

* Documents are in [test_docs.csv](./Lab1-Search-Engine/Data/test_docs.csv), 
each item has `doc_id`, `doc_url`, `doc_title` and `content`.
* Queries are in [test_querys.csv](./Lab1-Search-Engine/Data/test_querys.csv), 
each item has `query` and `query_id`.
* Submission format is shown in [submission.csv](./Lab1-Search-Engine/Data/submission.csv).

More details: [http://staff.ustc.edu.cn/~tongxu/webinfo/slides/exp1.pdf](http://staff.ustc.edu.cn/~tongxu/webinfo/slides/exp1.pdf)

## Lab2 Entity Recognition

A task of clinical named entity recognition (CNER) in CCKS 2019.

* Train set is given in [train.txt](./Lab2-Entity-Recognition/Data/train.txt),
each line is in JSON format with `originalText` and `entities`.
* Test set is given in [test.txt](./Lab2-Entity-Recognition/Data/test.txt),
each line is in JSON format with `originalText` and `textId`.
* Recognize entities in test set and record them in CSV format, 
each row includes `textId`, `label_type`, `start_pos`, `end_pos`.

More details: [http://staff.ustc.edu.cn/~tongxu/webinfo/slides/exp2.pdf](http://staff.ustc.edu.cn/~tongxu/webinfo/slides/exp2.pdf)

## Lab3 Recommender System
