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

### 1. Preprocess

You have to preprocess raw data `train.txt` and `test.txt` for CRF model.
You will get `train_word.txt` and `test_word.txt` after running this:

```shell
$ python3 preprocess.py
```

### 2. Rules

Recognize entities based on rules. 
You can edit `manual-rules.txt` to add rules.
Then run:

```shell
$ python3 rule.py
```

You will get `auto-rules.txt` and `rule.csv`.

### 3. CRF

Use CRF model to recognize entities:

```shell
$ python3 crf.py
```

You can get `submit.csv` as the result based on CRF model.

### 4. Fusion

Fuse `rule.csv` and `submit.csv`:

```shell
$ python3 fuse.py
```

You will get `fuse.csv` as finial result in `Data/`. 

### 5. Results

You can see my results and scores in `Data/`.

## Explanation

My report: [report-lab2.pdf](./report-lab2.pdf).
