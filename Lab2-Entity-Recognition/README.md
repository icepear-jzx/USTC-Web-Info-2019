# Lab2 Entity Recognition

A task of clinical named entity recognition (CNER) in CCKS 2019.

* Train set is given in [train.txt](./Data/train.txt),
each line is in JSON format with `originalText` and `entities`.
* Test set is given in [test.txt](./Data/test.txt),
each line is in JSON format with `originalText` and `textId`.
* Recognize entities in test set and record them in CSV format, 
each row includes `textId`, `label_type`, `start_pos`, `end_pos`.

More details: [http://staff.ustc.edu.cn/~tongxu/webinfo/slides/exp2.pdf](http://staff.ustc.edu.cn/~tongxu/webinfo/slides/exp2.pdf)

## Installation

```shell
$ pip3 install -r requirements.txt
```

## Usage

## Explanation
